"""Ghosts updated together around one shared schedule."""

import random
from typing import Optional

from app.gameplay.maze import Maze
from .ghost import Ghost
from .mode_schedule import ModeSchedule
from app.gameplay.ghosts.strategies import TargetingStrategy


class GhostGroup:
    """Own the ghosts and the schedule so their modes stay in sync."""
    def __init__(self, rng: Optional[random.Random] = None) -> None:
        """Create an empty group using an optional rng."""
        self._rng = rng if rng is not None else random.Random()
        self._schedule = ModeSchedule()
        self._ghosts: list[Ghost] = []

    @property
    def ghosts(self) -> tuple[Ghost, ...]:
        """Return the ghosts in creation order."""
        return tuple(self._ghosts)

    def add(self, spawn: tuple[int, int], speed: float,
            strategy: TargetingStrategy,
            pacman: tuple[float, float]) -> Ghost:
        """Create a ghost at spawn that follows the shared schedule."""
        ghost = Ghost(spawn, speed, strategy, pacman, self._schedule,
                      self._rng)
        self._ghosts.append(ghost)
        return ghost

    def frighten(self) -> None:
        """Frighten every ghost that is not returning or respawning."""
        self._schedule.frighten()
        for ghost in self._ghosts:
            ghost.frighten()

    def reset(self) -> None:
        """Put every ghost back on its spawn and restart the schedule."""
        self._schedule.reset()
        for ghost in self._ghosts:
            ghost.reset()

    def update(self, dt: float, maze: Maze,
               pacman: tuple[float, float]) -> None:
        """Advance the schedule and move ghosts toward Pac-Man's tile."""
        if dt <= 0:
            return
        self._schedule.update(dt)
        for ghost in self._ghosts:
            ghost.set_pacman_position(pacman)
            ghost.update(dt, maze)
