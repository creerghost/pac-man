"""Draw the current gameplay state through the shared Canvas contract."""

from math import ceil
from pathlib import Path

from app.core.canvas import Canvas
from app.core.ui import Color
from app.core.texture_manager import TextureManager

from .direction import Direction
from .game_state import GameState
from .ghosts import GhostState
from .tile import Tile


class GameView:
    """Render the maze, characters, and HUD."""

    def __init__(self) -> None:
        self._canvas: Canvas | None = None
        self._textures: TextureManager | None = None

    def render(self, canvas: Canvas, game: GameState) -> None:
        """Draw the maze, entities, and current HUD values."""
        maze = game.maze
        if maze.width <= 0 or maze.height <= 0:
            raise ValueError("The maze dimensions must be positive.")
        ui = canvas.ui
        size, offset_x, offset_y = ui.maze_layout(maze.width, maze.height)
        if (offset_x < 0 or offset_y < ui.font_small
                or offset_x + maze.width * size > ui.width
                or offset_y + maze.height * size > ui.height):
            raise ValueError("The window is too small for the maze and HUD.")

        canvas.mlx_clear_window(Color.BLACK)
        max_radius = (size - 1) // 2
        wall_thickness = max(1, size // 8)

        def wall(x: int, y: int) -> bool:
            return (0 <= x < maze.width and 0 <= y < maze.height
                    and maze.tile_at(x, y) == Tile.WALL)

        for y in range(maze.height):
            for x in range(maze.width):
                tile = maze.tile_at(x, y)
                left, top = offset_x + x * size, offset_y + y * size
                if tile == Tile.WALL:
                    # Only exposed edges are drawn, leaving connected wall
                    # regions dark on the inside.
                    if not wall(x, y - 1):
                        canvas.draw_rect(left, top, size, wall_thickness,
                                         Color.BLUE)
                    if not wall(x, y + 1):
                        canvas.draw_rect(left, top + size - wall_thickness,
                                         size, wall_thickness, Color.BLUE)
                    if not wall(x - 1, y):
                        canvas.draw_rect(left, top, wall_thickness, size,
                                         Color.BLUE)
                    if not wall(x + 1, y):
                        canvas.draw_rect(left + size - wall_thickness, top,
                                         wall_thickness, size, Color.BLUE)
                elif tile in (Tile.PACGUM, Tile.SUPER_PACGUM):
                    radius = (max(1, size // 10) if tile == Tile.PACGUM
                              else max(1, size // 4))
                    canvas.draw_circle(left + size // 2, top + size // 2,
                                       min(max_radius, radius), Color.WHITE)

        for x, y in maze.forty_two_tiles:
            canvas.draw_rect(offset_x + x * size, offset_y + y * size,
                             size, size, Color.BLACK)
        for x, y in maze.forty_two_tiles:
            left, top = offset_x + x * size, offset_y + y * size
            spacing = max(8, size)
            phase = int(game.animation_time * 32)
            first = (phase - left - top) % spacing
            for diagonal in range(first, 2 * size - 1, spacing):
                x_start = max(0, diagonal - size + 1)
                x_end = min(size - 1, diagonal)
                canvas.draw_line(left + x_start, top + diagonal - x_start,
                                 left + x_end, top + diagonal - x_end,
                                 Color.DARK_BLUE, 1)
            if (x, y - 1) not in maze.forty_two_tiles:
                canvas.draw_rect(left, top, size, wall_thickness, Color.BLUE)
            if (x, y + 1) not in maze.forty_two_tiles:
                canvas.draw_rect(left, top + size - wall_thickness,
                                 size, wall_thickness, Color.BLUE)
            if (x - 1, y) not in maze.forty_two_tiles:
                canvas.draw_rect(left, top, wall_thickness, size, Color.BLUE)
            if (x + 1, y) not in maze.forty_two_tiles:
                canvas.draw_rect(left + size - wall_thickness, top,
                                 wall_thickness, size, Color.BLUE)

        if self._canvas is not canvas:
            self._canvas = canvas
            self._textures = TextureManager(canvas)
        textures = self._textures
        assert textures is not None
        sprites = Path(__file__).resolve().parents[2] / "resources" / "sprites"

        def draw_entity(path: str, source: tuple[int, int, int, int],
                        x: float, y: float, angle: int = 0) -> None:
            texture = textures.get(str(sprites / path))
            left = int(offset_x + x * size)
            top = int(offset_y + y * size)
            canvas.draw_sprite(texture, source, (left, top, size, size), angle)

        progress = game.death_progress
        if progress is not None:
            frame = min(4, int(progress * 5))
            draw_entity("pacman_death.png", (frame * 362, 170, 362, 362),
                        game.pacman.x, game.pacman.y)
        else:
            frame = (0, 1, 2, 3)[int(game.animation_time * 8) % 4]
            angle = {Direction.RIGHT: 0, Direction.NONE: 0, Direction.UP: 90,
                     Direction.LEFT: 180, Direction.DOWN: 270}.get(
                         game.pacman.facing_direction, 0)
            draw_entity("pacman.png", (frame * 543, 90, 543, 543),
                        game.pacman.x, game.pacman.y, angle)

        for index, ghost in enumerate(game.ghosts):
            if ghost.state == GhostState.FRIGHTENED:
                frame = 4
            elif ghost.state in (GhostState.EATEN, GhostState.RESPAWNING):
                frame = 5
            else:
                frame = index % 4
            draw_entity("ghosts.png", (frame * 362, 170, 362, 362),
                        ghost.x, ghost.y)

        canvas.set_font(size=ui.font_hint)
        seconds = max(0, ceil(game.remaining_time))
        text = (f"SCORE: {game.score}   LIVES: {game.lives}   "
                f"TIME: {seconds}   LEVEL: {game.level}")
        canvas.mlx_string_put(ui.margin_x, 20, Color.WHITE, text)
