"""Blinky targets Pac-Man directly."""

from .targeting_strategy import TargetingStrategy


class BlinkyTargeting(TargetingStrategy):
    """Chase Pac-Man's current tile."""
    def target(self, pacman: tuple[int, int],
               ghost: tuple[int, int]) -> tuple[int, int]:
        """Return Pac-Man's current tile."""
        return pacman
