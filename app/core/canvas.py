from abc import ABC, abstractmethod
from webcolors import IntegerRGB


class Canvas(ABC):
    @abstractmethod
    def mlx_clear_window(self, color: IntegerRGB) -> None:
        pass

    @abstractmethod
    def draw_rect(self, x: int, y: int, w: int, h: int) -> None:
        pass

    @abstractmethod
    def draw_circle(self, x: int, y: int, radius: int,
                    color: IntegerRGB) -> None:
        pass

    @abstractmethod
    def _mlx_pixel_put(self, x: int, y: int, color: IntegerRGB) -> None:
        pass

    @abstractmethod
    def draw_line(x1: int, y1: int, x2: int, y2: int, color: IntegerRGB,
                  thickness: int) -> None:
        pass

    @abstractmethod
    def mlx_string_put(self, x: int, y: int,
                       color: IntegerRGB, text: str) -> None:
        pass
