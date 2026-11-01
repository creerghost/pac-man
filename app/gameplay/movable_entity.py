from .direction import Direction
from .maze import Maze
from abc import ABC, abstractmethod
from typing import Tuple


class MovableEntity(ABC):
    def __init__(self, pos: Tuple[float, float], speed: float):
        self._x, self._y = pos
        self._speed = speed
        self._direction = Direction.NONE

    @property
    def pos(self) -> Tuple[int, int]:
        return (round(self._x), round(self._y))

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def direction(self) -> Direction:
        return self._direction

    @property
    def speed(self) -> float:
        return self._speed

    @abstractmethod
    def update(self, dt: float, maze: Maze) -> None:
        pass

    def reset_position(self, x: float, y: float) -> None:
        self._x = float(x)
        self._y = float(y)
        self._direction = Direction.NONE

    def snap_to_corridor(self, new_direction: Direction) -> None:
        if new_direction in (Direction.UP, Direction.DOWN):
            self._x = float(round(self._x))
        elif new_direction in (Direction.LEFT, Direction.RIGHT):
            self._y = float(round(self._y))
