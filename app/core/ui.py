"""Centralized UI layout metrics, typography sizes, and color palette."""

from typing import Optional
from webcolors import IntegerRGB


class Color:
    """Shared RGB color constants for canvas rendering."""

    BLACK = IntegerRGB(0, 0, 0)
    BG_DARK = IntegerRGB(5, 5, 12)
    WHITE = IntegerRGB(255, 255, 255)
    YELLOW = IntegerRGB(255, 238, 0)
    GOLD = IntegerRGB(255, 225, 30)
    AMBER = IntegerRGB(255, 185, 130)
    ORANGE = IntegerRGB(255, 155, 35)
    RED = IntegerRGB(255, 55, 55)
    CHERRY = IntegerRGB(230, 25, 45)
    PINK = IntegerRGB(255, 105, 180)
    GREEN = IntegerRGB(0, 255, 120)
    STEM_GREEN = IntegerRGB(50, 185, 50)
    CYAN = IntegerRGB(0, 240, 255)
    BLUE = IntegerRGB(33, 33, 222)
    NEON_BLUE = IntegerRGB(38, 140, 255)
    DARK_BLUE = IntegerRGB(14, 38, 85)
    DIVIDER = IntegerRGB(30, 65, 120)
    GRAY = IntegerRGB(150, 150, 150)
    MUTED = IntegerRGB(140, 155, 185)


class UI:
    """Screen dimensions, typography, and layout helpers."""

    def __init__(self, scale: float = 1.0) -> None:
        """Initialize UI metrics with the given resolution scale factor."""
        self.scale = scale
        self.font_path = "resources/fonts/PressStart2P-Regular.ttf"

        self.width = self.scaled(720)
        self.height = self.scaled(864)
        self.center_x = self.width // 2
        self.center_y = self.height // 2

        self.font_title = self.scaled(32)
        self.font_text = self.scaled(24)
        self.font_hint = self.scaled(16)
        self.font_small = self.scaled(8)

        self.margin_x = self.scaled(24)
        self.margin_y = self.scaled(72)

    def scaled(self, value: int) -> int:
        """Scale a base pixel value by the current UI scale factor."""
        return max(1, int(value * self.scale))

    def text_width(self, text: str, font_size: int) -> int:
        """Return pixel width of a string for the monospace arcade font."""
        return len(text) * font_size

    def center_text_x(self, text: str, font_size: int, area_left: int = 0,
                      area_width: Optional[int] = None) -> int:
        """Return x coordinate that centers text horizontally in an area."""
        span = self.width if area_width is None else area_width
        return area_left + (span - self.text_width(text, font_size)) // 2

    def right_text_x(self, text: str, font_size: int,
                     right_edge: Optional[int] = None) -> int:
        """Return x coordinate that right-aligns text to a boundary."""
        edge = (
            self.width - self.margin_x if right_edge is None else right_edge
        )
        return edge - self.text_width(text, font_size)

    def line_y(self, index: int, font_size: int, start_y: Optional[int] = None,
               gap: int = 16) -> int:
        """Return y coordinate for the N-th row in a vertical list."""
        base_y = self.margin_y if start_y is None else start_y
        return base_y + index * (font_size + self.scaled(gap))

    def maze_layout(self, maze_cols: int,
                    maze_rows: int) -> tuple[int, int, int]:
        """Return (tile_size, offset_x, offset_y) fitting maze on screen."""
        avail_w = self.width - 2 * self.margin_x
        avail_h = self.height - 2 * self.margin_y
        tile_size = max(
            4,
            min(avail_w // max(1, maze_cols), avail_h // max(1, maze_rows)),
        )
        offset_x = (self.width - maze_cols * tile_size) // 2
        offset_y = (self.height - maze_rows * tile_size) // 2
        return tile_size, offset_x, offset_y
