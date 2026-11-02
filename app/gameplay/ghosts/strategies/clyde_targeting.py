"""Clyde alternates between pursuit and retreat."""

from .targeting_strategy import TargetingStrategy


class ClydeTargeting(TargetingStrategy):
    """Chase from a distance and retreat when close."""
    def __init__(self, corner: tuple[int, int]) -> None:
        """Set Clyde's retreat corner."""
        self._corner = corner

    def target(self, pacman: tuple[int, int],
               ghost: tuple[int, int]) -> tuple[int, int]:
        """Return pacman when over eight tiles away, else the corner."""
        distance = (pacman[0] - ghost[0]) ** 2 + (pacman[1] - ghost[1]) ** 2
        return pacman if distance > 64 else self._corner
