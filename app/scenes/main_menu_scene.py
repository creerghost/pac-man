"""Main menu and navigation to the game's screens."""

from typing import Any

from app.core.canvas import Canvas
from app.core.command import Command
from app.core.scene import Scene
from app.core.transition import Transition
from app.core.ui import Color
from app.io import GameConfig


class MainMenuScene(Scene):
    """Let players choose a destination using the keyboard."""

    _options = (
        ("START GAME", Transition.START_GAME),
        ("VIEW HIGHSCORES", Transition.OPEN_HIGHSCORES),
        ("INSTRUCTIONS", Transition.OPEN_INSTRUCTIONS),
        ("EXIT", Transition.EXIT_APP),
    )
    _team_name = r"B/\AD[I]M[I]P"

    def __init__(self, config: GameConfig) -> None:
        super().__init__(config)
        self._selected = 0
        self._next = Transition.NONE

    def on_enter(self, payload: Any) -> None:
        """Select the first option when opening the menu."""
        self._selected = 0
        self._next = Transition.NONE

    def on_exit(self) -> None:
        """Leave the main menu."""

    def handle_command(self, command: Command) -> None:
        """Move the selection or activate the selected option."""
        if command == Command.UP:
            self._selected = (self._selected - 1) % len(self._options)
        elif command == Command.DOWN:
            self._selected = (self._selected + 1) % len(self._options)
        elif command == Command.CONFIRM:
            self._next = self._options[self._selected][1]

    def update(self, dt: float) -> tuple[Transition, Any]:
        """Return and clear the pending transition."""
        transition, self._next = self._next, Transition.NONE
        return transition, None

    def render(self, canvas: Canvas) -> None:
        """Draw the menu, its selection, and team name."""
        ui = canvas.ui
        canvas.mlx_clear_window(Color.BLACK)
        canvas.set_font(size=ui.font_title)
        title = "PAC-MAN"
        canvas.mlx_string_put(ui.center_text_x(title, ui.font_title),
                              ui.margin_y, Color.YELLOW, title)
        canvas.set_font(size=ui.font_text)
        for index, (label, _) in enumerate(self._options):
            text = f"> {label} <" if index == self._selected else label
            color = Color.YELLOW if index == self._selected else Color.WHITE
            y = ui.line_y(index, ui.font_text,
                          start_y=ui.scaled(250), gap=28)
            canvas.mlx_string_put(ui.center_text_x(text, ui.font_text),
                                  y, color, text)
        canvas.set_font(size=ui.font_hint)
        hint = "UP / DOWN: SELECT    ENTER: CONFIRM"
        canvas.mlx_string_put(ui.center_text_x(hint, ui.font_hint),
                              ui.height - ui.scaled(120), Color.MUTED, hint)
        canvas.set_font(size=ui.font_small)
        canvas.mlx_string_put(ui.margin_x, ui.height - ui.scaled(24),
                              Color.MUTED, self._team_name)
