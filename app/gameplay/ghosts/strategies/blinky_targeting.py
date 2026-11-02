"""Blinky targets Pac-Man directly."""

from .targeting_strategy import TargetingStrategy


class BlinkyTargeting(TargetingStrategy):
    """Chase Pac-Man's current tile."""
    def target(self, pacman: tuple[float, float],
               ghost: tuple[int, int]) -> tuple[float, float]:
        """Return Pac-Man's current tile."""
        return pacman
