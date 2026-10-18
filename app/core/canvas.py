from abc import ABC, abstractmethod
from typing import Optional
from webcolors import IntegerRGB


class Canvas(ABC):
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
