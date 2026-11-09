"""Gameplay scene coordinating game state, input, view, and pause menu."""

from typing import Any

from app.core.canvas import Canvas
from app.core.command import Command
from app.core.scene import Scene
from app.core.transition import Transition
from app.core.ui import Color
from app.gameplay import Direction, GameState, GameView
from app.io import GameConfig


class GameplayScene(Scene):
    """Visual wrapper and controller for the core gameplay session."""

    _pause_options = ("RESUME", "MAIN MENU")

    def __init__(self, config: GameConfig) -> None:
        """Initialize the gameplay scene with view and game state."""
        super().__init__(config)
        self.view = GameView()
        self.state = GameState(config)
        self.is_paused = False
        self._selected_pause = 0
        self._next = Transition.NONE

    def on_enter(self, payload: Any) -> None:
        """Start a fresh game session whenever entering the scene."""
        self.state = GameState(self.config)
        self.is_paused = False
        self._selected_pause = 0
        self._next = Transition.NONE

    def on_exit(self) -> None:
        """Leave the gameplay scene."""
        self.is_paused = False

    def handle_command(self, command: Command) -> None:
        """Process movement, pause menu navigation, and cheat commands."""
        if self.is_paused:
            self._handle_pause_command(command)
            return

        if command.name in Direction.__members__:
            self.state.set_direction(Direction[command.name])
        elif command in (Command.PAUSE, Command.CANCEL):
            self.is_paused = True
            self._selected_pause = 0
        elif command == Command.CHEAT_INVINCIBLE:
            self.state.toggle_invincible_cheat()
        elif command == Command.CHEAT_SKIP_LEVEL:
            self.state.skip_level_cheat()
        elif command == Command.CHEAT_FREEZE:
            self.state.toggle_freeze_cheat()
        elif command == Command.CHEAT_LIFE:
            self.state.add_life_cheat()
        elif command == Command.CHEAT_SPEED:
            self.state.toggle_speed_cheat()

    def _handle_pause_command(self, command: Command) -> None:
        """Navigate or select options inside the pause menu."""
        if command == Command.UP:
            self._selected_pause = (self._selected_pause - 1) % len(
                self._pause_options
            )
        elif command == Command.DOWN:
            self._selected_pause = (self._selected_pause + 1) % len(
                self._pause_options
            )
        elif command == Command.CONFIRM:
            if self._selected_pause == 0:
                self.is_paused = False
            else:
                self._next = Transition.BACK_TO_MENU
        elif command in (Command.PAUSE, Command.CANCEL):
            self.is_paused = False

    def update(self, dt: float) -> tuple[Transition, Any]:
        """Advance game simulation or return scene transitions."""
        if self._next != Transition.NONE:
            transition, self._next = self._next, Transition.NONE
            return transition, None

        if not self.is_paused:
            self.state.update(dt)
            if self.state.is_game_over:
                return Transition.GAME_OVER, self.state.score
            if self.state.is_victory:
                return Transition.VICTORY, self.state.score

        return Transition.NONE, None

    def render(self, canvas: Canvas) -> None:
        """Draw the game state through GameView and pause overlay if paused."""
        self.view.render(canvas, self.state)
        if self.is_paused:
            self._render_pause_menu(canvas)

    def _render_pause_menu(self, canvas: Canvas) -> None:
        """Draw the pause overlay."""
        ui = canvas.ui
        canvas.set_font(size=ui.font_title)
        title = "PAUSED"
        canvas.mlx_string_put(ui.center_text_x(title, ui.font_title),
                              ui.center_y - ui.scaled(80), Color.YELLOW, title)

        canvas.set_font(size=ui.font_text)
        for index, label in enumerate(self._pause_options):
            is_sel = index == self._selected_pause
            text = f"> {label} <" if is_sel else label
            color = Color.YELLOW if is_sel else Color.WHITE
            y = ui.center_y + index * ui.scaled(40)
            canvas.mlx_string_put(ui.center_text_x(text, ui.font_text),
                                  y, color, text)

        canvas.set_font(size=ui.font_hint)
        hint = "UP / DOWN: SELECT   ENTER: CONFIRM"
        canvas.mlx_string_put(
            ui.center_text_x(hint, ui.font_hint),
            ui.height - ui.margin_y,
            Color.MUTED,
            hint,
        )
