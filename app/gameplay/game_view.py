"""Draw the current gameplay state through the shared Canvas contract."""

from math import ceil

from webcolors import IntegerRGB

from app.core.canvas import Canvas
from app.core.ui import Color

from .game_state import GameState
from .ghosts import GhostState
from .tile import Tile


class GameView:
    """Render a game state using the canvas's shared UI metrics."""

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
        for y in range(maze.height):
            for x in range(maze.width):
                tile = maze.tile_at(x, y)
                left, top = offset_x + x * size, offset_y + y * size
                if tile == Tile.WALL:
                    canvas.draw_rect(left, top, size, size, Color.BLUE)
                elif tile in (Tile.PACGUM, Tile.SUPER_PACGUM):
                    radius = (size // 10 if tile == Tile.PACGUM
                              else max(1, size // 4))
                    canvas.draw_circle(left + size // 2, top + size // 2,
                                       min(max_radius, radius), Color.WHITE)

        def draw_entity(x: float, y: float, color: IntegerRGB) -> None:
            canvas.draw_circle(int(offset_x + (x + 0.5) * size),
                               int(offset_y + (y + 0.5) * size),
                               min(max_radius, max(1, size * 2 // 5)), color)

        draw_entity(game.pacman.x, game.pacman.y, Color.YELLOW)
        ghost_colors = (Color.RED, Color.PINK, Color.CYAN, Color.ORANGE)
        for index, ghost in enumerate(game.ghosts):
            color = ghost_colors[index % len(ghost_colors)]
            if ghost.state == GhostState.FRIGHTENED:
                color = Color.NEON_BLUE
            elif ghost.state in (GhostState.EATEN, GhostState.RESPAWNING):
                color = Color.WHITE
            draw_entity(ghost.x, ghost.y, color)

        canvas.set_font(size=ui.font_small)
        seconds = max(0, ceil(game.remaining_time))
        text = (f"SCORE: {game.score}   LIVES: {game.lives}   "
                f"TIME: {seconds}   LEVEL: {game.level}")
        canvas.mlx_string_put(ui.margin_x, 0, Color.WHITE, text)
