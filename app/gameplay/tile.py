from enum import Enum


class Tile(Enum):
    """What occupies one cell of the maze grid."""
    WALL = 0
    EMPTY = 1
    PACGUM = 2
    SUPER_PACGUM = 3
