from typing import Any

from webcolors import IntegerRGB, name_to_rgb

from app.core.canvas import Canvas
from app.core.command import Command
from app.core.scene import Scene
from app.core.transition import Transition
from app.io.config import GameConfig

DIRECTIONS: dict[Command, tuple[int, int]] = {
    Command.UP: (0, -1), Command.DOWN: (0, 1),
    Command.LEFT: (-1, 0), Command.RIGHT: (1, 0)}

BLACK: IntegerRGB = name_to_rgb("black")
BLUE: IntegerRGB = name_to_rgb("blue")
YELLOW: IntegerRGB = name_to_rgb("yellow")
RED: IntegerRGB = name_to_rgb("red")
WHITE: IntegerRGB = name_to_rgb("white")


class FirstScene(Scene):
    """Temporary gameplay scene for checking the ending screens."""

    def __init__(self, config: GameConfig, width: int = 720,
                 height: int = 864) -> None:
        super().__init__(config)
        self._width = width
        self._height = height
        self._speed = 200.0
        self._radius = 20
        self._pellet_radius = 7
        self._hazard_radius = 25
        self._hazard = (width // 2, height // 4)
        self.on_enter(None)

    def on_enter(self, payload: Any) -> None:
        """Reset the test player, pellets, and score."""
        self._x, self._y = self._width / 2, self._height / 2
        self._direction = (0, 0)
        self._score = 0
        self._next = Transition.NONE
        self._pellets = [
            (self._width // 4, self._height // 3),
            (3 * self._width // 4, self._height // 3),
            (self._width // 4, 2 * self._height // 3),
            (3 * self._width // 4, 2 * self._height // 3),
        ]

    def on_exit(self) -> None:
        """Leave the temporary test scene."""

    def handle_command(self, command: Command) -> None:
        """Move with arrows/WASD or return to the menu with Escape."""
        self._direction = DIRECTIONS.get(command, self._direction)
        if command == Command.CANCEL:
            self._next = Transition.BACK_TO_MENU

    def _touches(self, pos: tuple[int, int], radius: int) -> bool:
        return ((self._x - pos[0]) ** 2 + (self._y - pos[1]) ** 2
                <= (self._radius + radius) ** 2)

    def update(self, dt: float) -> tuple[Transition, Any]:
        """Move in small steps to detect collisions even on slow frames."""
        if self._next != Transition.NONE:
            transition, self._next = self._next, Transition.NONE
            return transition, None
        distance = max(0.0, dt) * self._speed
        while distance > 0:
            step = min(distance, self._radius)
            self._x = min(max(self._x + self._direction[0] * step,
                              self._radius), self._width - self._radius)
            self._y = min(max(self._y + self._direction[1] * step,
                              self._radius), self._height - self._radius)
            if self._touches(self._hazard, self._hazard_radius):
                return Transition.GAME_OVER, self._score
            remaining = []
            for pellet in self._pellets:
                if self._touches(pellet, self._pellet_radius):
                    self._score += self.config.points_per_pacgum
                else:
                    remaining.append(pellet)
            self._pellets = remaining
            if not self._pellets:
                return Transition.VICTORY, self._score
            distance -= step
        return Transition.NONE, None

    def render(self, canvas: Canvas) -> None:
        """Draw pellets, hazard, player, score, and basic controls."""
        canvas.mlx_clear_window(BLACK)
        canvas.set_font(size=canvas.ui.font_hint)
        for x, y in self._pellets:
            canvas.draw_circle(x, y, self._pellet_radius, WHITE)
        canvas.draw_circle(*self._hazard, self._hazard_radius, RED)
        canvas.draw_circle(int(self._x), int(self._y), self._radius, YELLOW)
        canvas.mlx_string_put(24, 24, WHITE, f"SCORE: {self._score}")
        canvas.mlx_string_put(24, self._height - 64, WHITE,
                              "COLLECT WHITE DOTS; AVOID RED")
        canvas.mlx_string_put(24, self._height - 40, WHITE,
                              "ARROWS / WASD: MOVE   ESC: MENU")


class SecondScene(Scene):
    def __init__(self, config: GameConfig, width: int = 800,
                 height: int = 600) -> None:
        self.config = config
        self._width = width
        self._height = height
        self._position = (width // 2, height // 2)
        self._next = Transition.NONE
        self._transitions = {Command.CONFIRM: Transition.START_GAME,
                             Command.CANCEL: Transition.EXIT_APP}

    def on_enter(self, payload: Any) -> None:
        self._position = payload
        self._next = Transition.NONE

    def on_exit(self) -> None:
        pass

    def handle_command(self, command: Command) -> None:
        self._next = self._transitions.get(command, self._next)

    def update(self, dt: float) -> tuple[Transition, Any]:
        transition, self._next = self._next, Transition.NONE
        return transition, None

    def render(self, canvas: Canvas) -> None:
        canvas.mlx_clear_window(BLUE)
        canvas.draw_circle(self._position[0], self._position[1], 30, RED)
        canvas.mlx_string_put(40, self._height - 40, WHITE,
                              f"Circle left at {self._position}  "
                              "ENTER/ESC: back")
