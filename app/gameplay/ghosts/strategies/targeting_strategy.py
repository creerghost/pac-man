"""Contract for choosing a ghost's chase target."""

from abc import ABC, abstractmethod


class TargetingStrategy(ABC):
    """Calculate a target from Pac-Man's and the ghost's tile."""
    @abstractmethod
    def target(self, pacman: tuple[int, int],
               ghost: tuple[int, int]) -> tuple[int, int]:
        """Return the chase target tile for pacman and ghost."""
        pass
