"""Abstract base class for all movable entities on the maze grid."""

from abc import ABC, abstractmethod
from typing import Tuple

from .direction import Direction
from .maze import Maze


class MovableEntity(ABC):
    """Abstract base class for entities with continuous grid movement."""

    def __init__(self, pos: Tuple[float, float], speed: float) -> None:
        """Initialize position and speed of the movable entity."""
        self._x, self._y = pos
        self._speed = speed
        self._direction = Direction.NONE

    @property
    def pos(self) -> Tuple[int, int]:
        """Compute current discrete tile coordinates on the maze."""
        return (round(self._x), round(self._y))

    @property
    def x(self) -> float:
        """Return the current horizontal sub-pixel coordinate."""
        return self._x

    @property
    def y(self) -> float:
        """Return the current vertical sub-pixel coordinate."""
        return self._y

    @property
    def direction(self) -> Direction:
        """Return the current movement direction."""
        return self._direction

    @property
    def speed(self) -> float:
        """Return the movement speed in tiles per second."""
        return self._speed

    @abstractmethod
    def update(self, dt: float, maze: Maze) -> None:
        """Update entity state and position for the elapsed time."""
        pass

    def reset_position(self, x: float, y: float) -> None:
        """Reset entity position and stop movement."""
        self._x = float(x)
        self._y = float(y)
        self._direction = Direction.NONE

    def snap_to_corridor(self, new_direction: Direction) -> None:
        """Align perpendicular coordinate to corridor centre."""
        if new_direction in (Direction.UP, Direction.DOWN):
            self._x = float(round(self._x))
        elif new_direction in (Direction.LEFT, Direction.RIGHT):
            self._y = float(round(self._y))
