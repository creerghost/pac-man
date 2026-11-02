"""Pinky targets ahead of Pac-Man."""

from typing import Callable

from app.gameplay.direction import Direction
from .targeting_strategy import TargetingStrategy


class PinkyTargeting(TargetingStrategy):
    """Ambush Pac-Man four tiles ahead."""
    def __init__(self, direction: Callable[[], Direction]) -> None:
        """Read Pac-Man's current direction using direction."""
        self._direction = direction

    def target(self, pacman: tuple[int, int],
               ghost: tuple[int, int]) -> tuple[int, int]:
        """Return the tile four steps ahead of pacman."""
        dx, dy = self._direction().offset
        return pacman[0] + 4 * dx, pacman[1] + 4 * dy
