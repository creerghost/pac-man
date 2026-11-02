"""Inky targets a reflection based on Blinky."""

from typing import Callable

from app.gameplay.direction import Direction
from .targeting_strategy import TargetingStrategy


class InkyTargeting(TargetingStrategy):
    """Reflect Blinky across the tile two steps ahead of Pac-Man."""
    def __init__(self, direction: Callable[[], Direction],
                 blinky: Callable[[], tuple[int, int]]) -> None:
        """Read Pac-Man's direction and Blinky's tile using callbacks."""
        self._direction = direction
        self._blinky = blinky

    def target(self, pacman: tuple[int, int],
               ghost: tuple[int, int]) -> tuple[int, int]:
        """Return Blinky's reflection across the tile ahead of pacman."""
        dx, dy = self._direction().offset
        bx, by = self._blinky()
        return 2 * (pacman[0] + 2 * dx) - bx, 2 * (pacman[1] + 2 * dy) - by
