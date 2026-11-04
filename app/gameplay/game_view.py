"""Draw the maze and its occupants through the Canvas contract."""

from math import ceil
from typing import Callable

from webcolors import name_to_rgb

from app.core.canvas import Canvas
from app.io.config import GameConfig

from .maze import Maze
from .pacman import Pacman
from .tile import Tile


class GameView:
    """Render a maze inside a window, leaving space for its HUD."""
    def __init__(self, width: int, height: int, config: GameConfig) -> None:
        """Use the window dimensions and HUD height to lay out the view."""
        self._width = width
        self._height = height
        self._hud_height = config.hud_height

    def render(self, canvas: Canvas, maze: Maze, pacman: Pacman, score: int,
               lives: int, remaining_time: float, level: int) -> None:
        """Draw the current maze, player and HUD values onto canvas."""
        if maze.width <= 0 or maze.height <= 0:
            raise ValueError("The maze dimensions must be positive.")
        default_height = GameConfig.DEFAULT_HUD_HEIGHT
        if (self._width >= maze.width
                and self._height - self._hud_height < maze.height
                and self._height - default_height >= maze.height):
            print("[Config Warning] 'hud_height' leaves no room for the "
                  f"maze. Using default {default_height}.")
            self._hud_height = default_height
        available_height = self._height - self._hud_height
        size = min(self._width // maze.width, available_height // maze.height)
        if size < 1:
            raise ValueError("The window is too small for the maze and HUD.")
        offset_x = (self._width - maze.width * size) // 2
        offset_y = (self._hud_height
                    + (available_height - maze.height * size) // 2)

        blue, white = name_to_rgb("blue"), name_to_rgb("white")
        # shortcut: tiles under 3px cannot show two dot sizes; add zoom later.
        max_radius = (size - 1) // 2
        dot_radius = min(max_radius, size // 10)
        super_radius = min(max_radius, max(1, size // 4))
        draw: dict[Tile, Callable[[int, int], None]] = {
            Tile.WALL: lambda x, y: canvas.draw_rect(x, y, size, size, blue),
            Tile.PACGUM: lambda x, y: canvas.draw_circle(
                x + size // 2, y + size // 2, dot_radius, white),
            Tile.SUPER_PACGUM: lambda x, y: canvas.draw_circle(
                x + size // 2, y + size // 2, super_radius, white),
            Tile.EMPTY: lambda x, y: None,
        }
        # shortcut: full redraw is slow; cache walls when Canvas supports it.
        canvas.mlx_clear_window(name_to_rgb("black"))
        for y in range(maze.height):
            for x in range(maze.width):
                draw[maze.tile_at(x, y)](offset_x + x * size,
                                         offset_y + y * size)
        player_x = int(offset_x + (pacman.x + 0.5) * size)
        player_y = int(offset_y + (pacman.y + 0.5) * size)
        player_radius = min(max_radius, max(1, size * 2 // 5))
        canvas.draw_circle(player_x, player_y, player_radius,
                           name_to_rgb("yellow"))
        seconds = max(0, ceil(remaining_time))
        text = (f"SCORE: {score}   LIVES: {lives}   "
                f"TIME: {seconds}   LEVEL: {level}")
        canvas.mlx_string_put(0, 0, white, text)
