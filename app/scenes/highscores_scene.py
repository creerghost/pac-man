"""Highscores scene displaying top-10 player records."""

from typing import Any

from app.core.canvas import Canvas
from app.core.command import Command
from app.core.scene import Scene
from app.core.transition import Transition
from app.core.ui import Color
from app.io import GameConfig, HighscoreRecord, HighscoreRepository


class HighscoresScene(Scene):
    """Display the top-10 highscores table and return to menu on input."""

    def __init__(self, config: GameConfig) -> None:
        """Initialize the highscores scene and repository."""
        super().__init__(config)
        self._repo = HighscoreRepository(config.highscore_filename)
        self._records: list[HighscoreRecord] = []
        self._next_transition = Transition.NONE

    def on_enter(self, payload: Any) -> None:
        """Reload the latest top-10 records when entering the scene."""
        self._records = self._repo.read_all()[:self._repo.MAX_RECORDS]
        self._next_transition = Transition.NONE

    def on_exit(self) -> None:
        """Leave the highscores scene."""

    def handle_command(self, command: Command) -> None:
        """Return to the main menu on confirm or cancel."""
        if command in (Command.CANCEL, Command.CONFIRM):
            self._next_transition = Transition.BACK_TO_MENU

    def update(self, dt: float) -> tuple[Transition, Any]:
        """Return and clear the pending scene transition."""
        transition = self._next_transition
        self._next_transition = Transition.NONE
        return transition, None

    @staticmethod
    def _ordinal(rank: int) -> str:
        """Format a 1-based rank number as an ordinal string (1st, 2nd)."""
        suffixes = {1: "st", 2: "nd", 3: "rd"}
        suffix = ("th" if 11 <= rank % 100 <= 13
                  else suffixes.get(rank % 10, "th"))
        return f"{rank}{suffix}"

    def render(self, canvas: Canvas) -> None:
        """Render the highscores title, top-10 list, and return hint."""
        canvas.mlx_clear_window(Color.BLACK)
        ui = canvas.ui

        title = "HIGH SCORES"
        canvas.set_font(size=ui.font_title)
        canvas.mlx_string_put(ui.center_text_x(title, ui.font_title),
                              ui.margin_y, Color.YELLOW, title)

        canvas.set_font(size=ui.font_text)
        if not self._records:
            empty_msg = "NO SCORES YET"
            canvas.mlx_string_put(ui.center_text_x(empty_msg, ui.font_text),
                                  ui.center_y, Color.MUTED, empty_msg)
        else:
            start_y = ui.line_y(1, ui.font_title, gap=32)
            for index, record in enumerate(self._records):
                rank_num = index + 1
                row_y = ui.line_y(index, ui.font_text, start_y=start_y, gap=24)
                left_text = f"{self._ordinal(rank_num):<4} {record.nickname}"
                score_text = f"{record.score}pts"

                canvas.mlx_string_put(ui.margin_x, row_y, Color.WHITE,
                                      left_text)
                canvas.mlx_string_put(ui.right_text_x(score_text,
                                                      ui.font_text),
                                      row_y, Color.WHITE, score_text)

        hint = "ENTER / ESC: BACK TO MENU"
        canvas.set_font(size=ui.font_hint)
        canvas.mlx_string_put(ui.center_text_x(hint, ui.font_hint),
                              ui.height - ui.margin_y, Color.MUTED, hint)
