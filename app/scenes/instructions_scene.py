"""Instructions for the game's objectives and controls."""

from typing import Any

from app.core.canvas import Canvas
from app.core.command import Command
from app.core.scene import Scene
from app.core.transition import Transition
from app.core.ui import Color
from app.io import GameConfig


class InstructionsScene(Scene):
    """Show the game objective, controls, and debug key bindings."""

    def __init__(self, config: GameConfig) -> None:
        super().__init__(config)
        self._next = Transition.NONE

    def on_enter(self, payload: Any) -> None:
        """Reset the pending transition when the screen opens."""
        self._next = Transition.NONE

    def on_exit(self) -> None:
        """Leave the instructions screen."""

    def handle_command(self, command: Command) -> None:
        """Return to the menu on Enter or Escape."""
        if command in (Command.CONFIRM, Command.CANCEL):
            self._next = Transition.BACK_TO_MENU

    def update(self, dt: float) -> tuple[Transition, Any]:
        """Return and clear the pending transition."""
        transition, self._next = self._next, Transition.NONE
        return transition, None

    def render(self, canvas: Canvas) -> None:
        """Draw the objective, movement, and debug controls."""
        ui = canvas.ui
        canvas.mlx_clear_window(Color.BLACK)
        canvas.set_font(size=ui.font_title)
        title = "INSTRUCTIONS"
        canvas.mlx_string_put(ui.center_text_x(title, ui.font_title),
                              ui.margin_y, Color.YELLOW, title)

        rows = (
            ("GOAL", Color.GOLD),
            ("EAT ALL PELLETS TO CLEAR EACH LEVEL.", Color.WHITE),
            ("AVOID GHOSTS AND BEAT THE CLOCK.", Color.WHITE),
            ("POWER PELLETS LET YOU EAT GHOSTS.", Color.WHITE),
            ("CONTROLS", Color.GOLD),
            ("ARROWS / WASD: MOVE", Color.WHITE),
            ("P / SPACE: PAUSE", Color.WHITE),
            ("CHEAT KEYS (DEBUG)", Color.GOLD),
            ("C: TOGGLE CHEAT MODE", Color.WHITE),
            ("1: INVINCIBLE    2: SKIP LEVEL", Color.WHITE),
            ("3: FREEZE GHOSTS  4: EXTRA LIFE", Color.WHITE),
            ("5: SPEED BOOST", Color.WHITE),
        )
        canvas.set_font(size=ui.font_hint)
        start_y = ui.margin_y + ui.scaled(72)
        for index, (line, color) in enumerate(rows):
            y = ui.line_y(index, ui.font_hint, start_y=start_y, gap=20)
            canvas.mlx_string_put(ui.margin_x, y, color, line)
        hint = "ENTER / ESC: BACK TO MENU"
        canvas.mlx_string_put(ui.center_text_x(hint, ui.font_hint),
                              ui.height - ui.margin_y, Color.MUTED, hint)
