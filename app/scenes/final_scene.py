"""Shared score entry and submission for final screens."""

from typing import Any

from app.core import Canvas, Color, Command, Scene, Transition
from app.io import GameConfig, HighscoreRepository


class BaseFinalScene(Scene):
    """Display a final score and save it under an entered player name.

    Subclasses provide a heading. The entry payload is a nonnegative integer
    score, as passed by the gameplay scene when it changes screens.
    """

    heading = "FINAL SCORE"
    max_name_length = 10

    def __init__(self, config: GameConfig) -> None:
        super().__init__(config)
        self._repository = HighscoreRepository(config.highscore_filename)
        self.name = ""
        self.score = 0
        self._next = Transition.NONE

    def on_enter(self, payload: Any) -> None:
        """Start a fresh score entry for the given final score."""
        if type(payload) is not int or payload < 0:
            raise ValueError("Final scene requires a nonnegative "
                             "integer score")
        self.score = payload
        self.name = ""
        self._next = Transition.NONE

    def on_exit(self) -> None:
        """Leave the final screen."""

    def handle_text(self, text: str) -> None:
        """Accept ASCII letters and digits up to the name length limit."""
        for char in text:
            if char.isascii() and char.isalnum():
                if len(self.name) < self.max_name_length:
                    self.name += char

    def handle_command(self, command: Command) -> None:
        """Delete the last character or submit a nonempty name."""
        if command == Command.DELETE:
            self.name = self.name[:-1]
        elif (command == Command.CONFIRM and self.name
              and self._next == Transition.NONE):
            self._repository.upsert_score(self.name, self.score)
            self._next = Transition.BACK_TO_MENU

    def update(self, dt: float) -> tuple[Transition, Any]:
        """Return the requested transition once."""
        transition, self._next = self._next, Transition.NONE
        return transition, None

    def render(self, canvas: Canvas) -> None:
        """Draw the final score and editable name."""
        ui = canvas.ui
        canvas.mlx_clear_window(Color.BLACK)
        canvas.set_font(size=ui.font_text)
        lines = (self.heading, f"SCORE: {self.score}", "ENTER YOUR NAME",
                 f"{self.name}_", "ENTER TO CONTINUE")
        for index, line in enumerate(lines):
            canvas.mlx_string_put(ui.center_text_x(line, ui.font_text),
                                  ui.line_y(index, ui.font_text,
                                            start_y=ui.margin_y, gap=24),
                                  Color.WHITE, line)
