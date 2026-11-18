"""Pygame texture implementation wrapping a pygame Surface."""

import pygame

from app.core import Texture


class PygameTexture(Texture):
    """Concrete texture for the Pygame platform."""

    def __init__(self, surface: pygame.Surface) -> None:
        self._surface = surface

    @property
    def surface(self) -> pygame.Surface:
        """Return underlying Pygame surface."""
        return self._surface

    @property
    def width(self) -> int:
        """Return image width."""
        return self._surface.get_width()

    @property
    def height(self) -> int:
        """Return image height."""
        return self._surface.get_height()
