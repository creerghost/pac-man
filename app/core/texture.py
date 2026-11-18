"""Abstract texture interface mirroring MLX image handle."""

from abc import ABC, abstractmethod


class Texture(ABC):
    """Abstract image texture."""

    @property
    @abstractmethod
    def width(self) -> int:
        """Return image width in pixels."""
        pass

    @property
    @abstractmethod
    def height(self) -> int:
        """Return image height in pixels."""
        pass
