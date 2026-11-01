"""Direction primitives and grid vector offsets."""

from enum import Enum
from typing import Tuple


class Direction(Enum):
    """Movement directions on a 2D tile grid."""

    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    NONE = (0, 0)

    @property
    def opposite(self) -> "Direction":
        """Return the 180-degree opposite direction."""
        opposites = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
            Direction.NONE: Direction.NONE,
        }
        return opposites[self]

    @property
    def offset(self) -> Tuple[int, int]:
        """Return the (dx, dy) vector offset on the grid."""
        return self.value
