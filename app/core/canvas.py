from abc import ABC, abstractmethod
from typing import Optional
from webcolors import IntegerRGB

from .texture import Texture
from .ui import UI


class Canvas(ABC):
    def __init__(self, ui: Optional[UI] = None) -> None:
        self.ui: UI = ui if ui is not None else UI()

    @abstractmethod
    def set_font(self, font_path: Optional[str] = None,
                 size: int = 20) -> None:
        pass

    @abstractmethod
    def mlx_clear_window(self, color: IntegerRGB) -> None:
        pass

    @abstractmethod
    def draw_rect(self, x: int, y: int, w: int, h: int,
                  color: IntegerRGB) -> None:
        pass

    @abstractmethod
    def draw_circle(self, x: int, y: int, radius: int,
                    color: IntegerRGB) -> None:
        pass

    @abstractmethod
    def _mlx_pixel_put(self, x: int, y: int, color: IntegerRGB) -> None:
        pass

    @abstractmethod
    def draw_line(self, x1: int, y1: int, x2: int, y2: int, color: IntegerRGB,
                  thickness: int) -> None:
        pass

    @abstractmethod
    def mlx_string_put(self, x: int, y: int,
                       color: IntegerRGB, text: str) -> None:
        pass

    @abstractmethod
    def load_texture(self, path: str) -> Texture:
        pass

    @abstractmethod
    def mlx_put_image_to_window(self, texture: Texture,
                                x: int, y: int) -> None:
        pass

    @abstractmethod
    def draw_sprite(self, texture: Texture, source: tuple[int, int, int, int],
                    destination: tuple[int, int, int, int],
                    angle: int = 0) -> None:
        """Draw a scaled, optionally rotated region of a texture."""
        pass
