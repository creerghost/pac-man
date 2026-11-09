from mazegenerator import MazeGenerator

from .maze import Maze
from .tile import Tile

SEALED = 15
EAST = 2
SOUTH = 4


class MazeAdapter(Maze):
    """A Maze built from the tile-converted output of a MazeGenerator."""
    def __init__(self, generator: MazeGenerator) -> None:
        self._grid = self._to_tiles(generator.maze)
        self._forty_two_tiles = self._find_forty_two(generator.maze)
        self._ghost_spawns = self._corners()
        for x, y in self._ghost_spawns:
            self.set_tile(x, y, Tile.SUPER_PACGUM)
        self._pacman_spawn = self._find_pacman_spawn()
        spawn_x, spawn_y = self._pacman_spawn
        self.set_tile(spawn_x, spawn_y, Tile.EMPTY)

    @property
    def width(self) -> int:
        return len(self._grid[0])

    @property
    def height(self) -> int:
        return len(self._grid)

    @property
    def forty_two_tiles(self) -> frozenset[tuple[int, int]]:
        """Return the wall tiles occupied by the generator's 42."""
        return self._forty_two_tiles

    def tile_at(self, x: int, y: int) -> Tile:
        if not self._in_bounds(x, y):
            return Tile.WALL
        return self._grid[y][x]

    def is_walkable(self, x: int, y: int) -> bool:
        return self.tile_at(x, y) is not Tile.WALL

    def set_tile(self, x: int, y: int, tile: Tile) -> None:
        if self._in_bounds(x, y):
            self._grid[y][x] = tile

    def pacgums_left(self) -> int:
        dots = (Tile.PACGUM, Tile.SUPER_PACGUM)
        return sum(tile in dots for row in self._grid for tile in row)

    @property
    def pacman_spawn(self) -> tuple[int, int]:
        return self._pacman_spawn

    @property
    def ghost_spawns(self) -> list[tuple[int, int]]:
        return self._ghost_spawns

    def _to_tiles(self, cells: list[list[int]]) -> list[list[Tile]]:
        """Convert wall-bitmask cells into a (2h+1) x (2w+1) tile grid."""
        h, w = len(cells), len(cells[0])
        grid = [[Tile.WALL] * (2 * w + 1) for _ in range(2 * h + 1)]
        for cy in range(h):
            for cx in range(w):
                mask = cells[cy][cx]
                if mask == SEALED:  # 42 cells
                    continue
                grid[2*cy+1][2*cx+1] = Tile.PACGUM
                if not mask & EAST:
                    grid[2*cy+1][2*cx+2] = Tile.PACGUM
                if not mask & SOUTH:
                    grid[2*cy+2][2*cx+1] = Tile.PACGUM
        return grid

    def _find_forty_two(
        self, cells: list[list[int]]
    ) -> frozenset[tuple[int, int]]:
        """Map each sealed generator cell to its corresponding wall tiles."""
        tiles = set()
        for cy, row in enumerate(cells):
            for cx, mask in enumerate(row):
                if mask == SEALED:
                    for y in range(2 * cy, 2 * cy + 3):
                        for x in range(2 * cx, 2 * cx + 3):
                            if self.tile_at(x, y) == Tile.WALL:
                                tiles.add((x, y))
        return frozenset(tiles)

    def _in_bounds(self, x: int, y: int) -> bool:
        """Return True if column x and row y lie inside the grid."""
        return 0 <= x < self.width and 0 <= y < self.height

    def _corners(self) -> list[tuple[int, int]]:
        """Return the four corner tiles of super-pacgums and ghost spawns."""
        left, top = 1, 1
        right, bottom = self.width - 2, self.height - 2
        return [(left, top), (right, top),
                (left, bottom), (right, bottom)]

    def _find_pacman_spawn(self) -> tuple[int, int]:
        """Return the walkable tile closest to the centre of the maze."""
        centre_x, centre_y = self.width // 2, self.height // 2
        walkable = [(x, y) for y in range(self.height)
                    for x in range(self.width) if self.is_walkable(x, y)]
        return min(walkable, key=lambda p: abs(p[0] - centre_x)
                   + abs(p[1] - centre_y))
