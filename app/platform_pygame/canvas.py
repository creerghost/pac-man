from typing import Optional
import pygame
from webcolors import IntegerRGB

from app.core import Canvas


class PygameCanvas(Canvas):
    def __init__(self, screen: Optional[pygame.Surface] = None,
                 default_font_path: Optional[str] = None,
                 default_size: int = 20) -> None:
        self.screen = screen
        self._current_font_path = default_font_path
        self._current_size = default_size
        self._fonts: dict[tuple[Optional[str], int], pygame.font.Font] = {}

    def set_font(self, font_path: Optional[str] = None,
                 size: int = 20) -> None:
        self._current_font_path = font_path
        self._current_size = size

    def _get_font(self, path: Optional[str], size: int) -> pygame.font.Font:
        key = (path, size)
        if key not in self._fonts:
            if not pygame.font.get_init():
                pygame.font.init()
            if path:
                try:
                    self._fonts[key] = pygame.font.Font(path, size)
                except (FileNotFoundError, pygame.error):
                    self._fonts[key] = pygame.font.Font(None, size)
            else:
                self._fonts[key] = pygame.font.Font(None, size)
        return self._fonts[key]

    def mlx_clear_window(self, color: IntegerRGB) -> None:
        if self.screen is not None:
            self.screen.fill((color.red, color.green, color.blue))

    def _mlx_pixel_put(self, x: int, y: int, color: IntegerRGB) -> None:
        if self.screen is not None:
            width, height = self.screen.get_size()
            if 0 <= x < width and 0 <= y < height:
                self.screen.set_at(
                    (x, y), (color.red, color.green, color.blue)
                )

    def draw_rect(self, x: int, y: int, w: int, h: int,
                  color: IntegerRGB) -> None:
        for dx in range(w):
            for dy in range(h):
                self._mlx_pixel_put(x + dx, y + dy, color)

    def draw_circle(self, x: int, y: int, radius: int,
                    color: IntegerRGB) -> None:
        r_squared = radius * radius
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx * dx + dy * dy <= r_squared:
                    self._mlx_pixel_put(x + dx, y + dy, color)

    def draw_line(self, x1: int, y1: int, x2: int, y2: int,
                  color: IntegerRGB, thickness: int = 1) -> None:
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        curr_x, curr_y = x1, y1
        while True:
            self._mlx_pixel_put(curr_x, curr_y, color)
            if curr_x == x2 and curr_y == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                curr_x += sx
            if e2 < dx:
                err += dx
                curr_y += sy

    def mlx_string_put(self, x: int, y: int,
                       color: IntegerRGB, text: str) -> None:
        if self.screen is not None:
            font = self._get_font(self._current_font_path, self._current_size)
            surface = font.render(
                text, True, (color.red, color.green, color.blue)
            )
            self.screen.blit(surface, (x, y))
