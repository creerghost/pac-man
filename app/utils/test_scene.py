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
    def __init__(self, config: GameConfig, width: int = 800,
                 height: int = 600) -> None:
        self.config = config
        self._width = width
        self._height = height
        self._x = width / 2
        self._y = height / 2
        self._direction = (0, 0)
        self._speed = 200.0
        self._radius = 20
        self._next = Transition.NONE
        self._transitions = {Command.CONFIRM: Transition.START_GAME,
                             Command.CANCEL: Transition.EXIT_APP}

    def on_enter(self, payload: Any) -> None:
        self._next = Transition.NONE

    def on_exit(self) -> None:
        pass

    def handle_command(self, command: Command) -> None:
        self._direction = DIRECTIONS.get(command, self._direction)
        self._next = self._transitions.get(command, self._next)

    def update(self, dt: float) -> tuple[Transition, Any]:
        low, high_x = self._radius, self._width - self._radius
        high_y = self._height - self._radius
        self._x += self._direction[0] * self._speed * dt
        self._y += self._direction[1] * self._speed * dt
        self._x = min(max(self._x, low), high_x)
        self._y = min(max(self._y, low), high_y)
        transition, self._next = self._next, Transition.NONE
        return transition, (int(self._x), int(self._y))

    def render(self, canvas: Canvas) -> None:
        canvas.mlx_clear_window(BLACK)
        for i in range(10):
            canvas.draw_rect(40 + i * 72, 40, 64, 32)
        canvas.draw_circle(int(self._x), int(self._y), self._radius, YELLOW)
        canvas.mlx_string_put(40, self._height - 40, WHITE,
                              "Arrows: move  ENTER: next scene  ESC: quit")


class SecondScene(Scene):
    def __init__(self, config: GameConfig, width: int = 800,
                 height: int = 600) -> None:
        self.config = config
        self._width = width
        self._height = height
        self._position = (width // 2, height // 2)
        self._next = Transition.NONE
        self._transitions = {Command.CONFIRM: Transition.BACK_TO_MENU,
                             Command.CANCEL: Transition.BACK_TO_MENU}

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
