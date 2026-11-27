from typing import Optional
import pygame
from webcolors import IntegerRGB

from app.core import Canvas, Texture, UI
from .texture import PygameTexture


class PygameCanvas(Canvas):
    def __init__(self, screen: Optional[pygame.Surface] = None,
                 ui: Optional[UI] = None) -> None:
        super().__init__(ui)
        self.screen = screen
        self._current_font_path: Optional[str] = self.ui.font_path
        self._current_size: int = self.ui.font_text
        self._fonts: dict[tuple[Optional[str], int], pygame.font.Font] = {}
        self._textures: dict[str, PygameTexture] = {}
        self._sprites: dict[tuple, pygame.Surface] = {}

    def set_font(self, font_path: Optional[str] = None,
                 size: int = 20) -> None:
        self._current_font_path = font_path or self.ui.font_path
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
        if self.screen is not None:
            pygame.draw.rect(
                self.screen,
                (color.red, color.green, color.blue),
                (x, y, w, h)
            )

    def draw_circle(self, x: int, y: int, radius: int,
                    color: IntegerRGB) -> None:
        if self.screen is not None:
            pygame.draw.circle(
                self.screen,
                (color.red, color.green, color.blue),
                (x, y),
                radius
            )

    def draw_line(self, x1: int, y1: int, x2: int, y2: int,
                  color: IntegerRGB, thickness: int = 1) -> None:
        if self.screen is not None:
            pygame.draw.line(
                self.screen,
                (color.red, color.green, color.blue),
                (x1, y1),
                (x2, y2),
                thickness
            )

    def mlx_string_put(self, x: int, y: int,
                       color: IntegerRGB, text: str) -> None:
        if self.screen is not None:
            font = self._get_font(self._current_font_path, self._current_size)
            surface = font.render(
                text, True, (color.red, color.green, color.blue)
            )
            self.screen.blit(surface, (x, y))

    def load_texture(self, path: str) -> Texture:
        if path not in self._textures:
            try:
                surface = pygame.image.load(path)
                if (pygame.display.get_init()
                        and pygame.display.get_surface() is not None):
                    surface = surface.convert_alpha()
            except (FileNotFoundError, pygame.error) as err:
                raise FileNotFoundError(
                    f"Failed to load texture at '{path}': {err}"
                ) from err
            self._textures[path] = PygameTexture(surface)
        return self._textures[path]

    def mlx_put_image_to_window(self, texture: Texture,
                                x: int, y: int) -> None:
        if self.screen is None:
            return
        if not isinstance(texture, PygameTexture):
            raise TypeError(
                f"Expected PygameTexture, got {type(texture).__name__}"
            )
        self.screen.blit(texture.surface, (x, y))

    def draw_sprite(self, texture: Texture, source: tuple[int, int, int, int],
                    destination: tuple[int, int, int, int],
                    angle: int = 0) -> None:
        if self.screen is None:
            return
        if not isinstance(texture, PygameTexture):
            raise TypeError(
                f"Expected PygameTexture, got {type(texture).__name__}"
            )
        x, y, width, height = destination
        key = (texture, source, width, height, angle)
        if key not in self._sprites:
            frame = texture.surface.subsurface(pygame.Rect(source))
            frame = pygame.transform.scale(frame, (width, height))
            self._sprites[key] = pygame.transform.rotate(frame, angle)
        self.screen.blit(self._sprites[key], (x, y))
