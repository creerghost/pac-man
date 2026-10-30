from abc import ABC, abstractmethod

from .tile import Tile


class Maze(ABC):
    """A grid of tiles that the game logic and the view read."""
    @property
    @abstractmethod
    def width(self) -> int:
        """Return the number of tile columns."""
        pass

    @property
    @abstractmethod
    def height(self) -> int:
        """Return the number of tile rows."""
        pass

    @abstractmethod
    def tile_at(self, x: int, y: int) -> Tile:
        """Return the tile at column x and row y, or WALL outside the grid."""
        pass

    @abstractmethod
    def is_walkable(self, x: int, y: int) -> bool:
        """Return True if Pac-Man or a ghost can stand on that tile."""
        pass

    @abstractmethod
    def set_tile(self, x: int, y: int, tile: Tile) -> None:
        """Replace the tile at x, y, e.g. with EMPTY once a pacgum is eaten."""
        pass

    @abstractmethod
    def pacgums_left(self) -> int:
        """Return how many PACGUM and SUPER_PACGUM tiles remain."""
        pass

    @property
    @abstractmethod
    def pacman_spawn(self) -> tuple[int, int]:
        """Return the tile where Pac-Man starts and respawns after a death."""
        pass

    @property
    @abstractmethod
    def ghost_spawns(self) -> list[tuple[int, int]]:
        """Return one start tile per ghost, in ghost creation order."""
        pass
