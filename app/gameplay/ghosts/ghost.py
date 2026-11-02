"""Ghost movement, state transitions, and navigation."""

from collections import deque
import math
import random
from typing import Callable, Optional

from app.gameplay.direction import Direction
from app.gameplay.maze import Maze
from app.gameplay.movable_entity import MovableEntity
from .ghost_state import GhostState
from .mode_schedule import ModeSchedule
from .strategies import TargetingStrategy

Chooser = Callable[[Maze, tuple[int, int]], Direction]


class Ghost(MovableEntity):
    """A ghost that moves autonomously using an injected chase strategy."""
    def __init__(self, spawn: tuple[int, int], speed: float,
                 strategy: TargetingStrategy,
                 pacman: Callable[[], tuple[int, int]],
                 schedule: ModeSchedule,
                 rng: Optional[random.Random] = None) -> None:
        """Place a ghost at spawn that follows the shared schedule."""
        super().__init__((float(spawn[0]), float(spawn[1])), speed)
        self._spawn = spawn
        self._pacman = pacman
        self._schedule = schedule
        self._rng = rng if rng is not None else random.Random()
        self._override: Optional[GhostState] = None
        self._respawn_left = 0.0
        self._speed_factors = {
            GhostState.FRIGHTENED: 0.5,
            GhostState.EATEN: 2.0,
            GhostState.RESPAWNING: 0.0,
        }
        self._choosers: dict[GhostState, Chooser] = {
            GhostState.CHASE: lambda maze, pos: self._toward(
                maze, pos, strategy.target(self._pacman(), pos)),
            GhostState.SCATTER: lambda maze, pos: self._toward(
                maze, pos, self._spawn),
            GhostState.FRIGHTENED: self._flee,
            GhostState.EATEN: self._path_home,
        }

    @property
    def state(self) -> GhostState:
        """Return this ghost's own state, or else the shared phase."""
        if self._override is None:
            return self._schedule.mode
        return self._override

    @property
    def speed(self) -> float:
        """Return the speed in tiles per second for the current state."""
        return self._speed * self._speed_factors.get(self.state, 1.0)

    def frighten(self) -> None:
        """Become frightened unless returning or respawning."""
        if self._override not in (GhostState.EATEN, GhostState.RESPAWNING):
            self._override = GhostState.FRIGHTENED

    def eat(self) -> None:
        """Send a frightened ghost back to its spawn."""
        if self.state == GhostState.FRIGHTENED:
            self._override = GhostState.EATEN

    def reset(self) -> None:
        """Put the ghost back on its spawn in the shared phase."""
        self.reset_position(*self._spawn)
        self._override = None
        self._respawn_left = 0.0

    def _directions(self, maze: Maze, pos: tuple[int, int]) -> list[Direction]:
        """Return legal directions from the tile pos in stable order."""
        return [d for d in Direction if d != Direction.NONE and
                maze.is_walkable(pos[0] + d.offset[0], pos[1] + d.offset[1])]

    def _forward(self, maze: Maze, pos: tuple[int, int]) -> list[Direction]:
        """Return legal directions except reversing, unless at a dead end."""
        directions = self._directions(maze, pos)
        forward = [d for d in directions if d != self._direction.opposite]
        return forward or directions

    @staticmethod
    def _distance(pos: tuple[int, int], direction: Direction,
                  target: tuple[int, int]) -> int:
        """Return squared distance from the tile after pos to target."""
        dx, dy = direction.offset
        return (pos[0] + dx - target[0]) ** 2 + (pos[1] + dy - target[1]) ** 2

    def _toward(self, maze: Maze, pos: tuple[int, int],
                target: tuple[int, int]) -> Direction:
        """Return the forward direction whose next tile is nearest target."""
        directions = self._forward(maze, pos)
        if not directions:
            return Direction.NONE
        return min(directions, key=lambda d: self._distance(pos, d, target))

    def _flee(self, maze: Maze, pos: tuple[int, int]) -> Direction:
        """Pick a random direction that does not bring the ghost closer."""
        pacman = self._pacman()
        here = self._distance(pos, Direction.NONE, pacman)
        away = [d for d in self._directions(maze, pos)
                if self._distance(pos, d, pacman) >= here]
        choices = ([d for d in away if d != self._direction.opposite] or away
                   or self._forward(maze, pos))
        return self._rng.choice(choices) if choices else Direction.NONE

    def _path_home(self, maze: Maze, pos: tuple[int, int]) -> Direction:
        """Find the first step on a shortest walkable path to spawn."""
        queue: deque[tuple[tuple[int, int], Direction]] = deque()
        seen = {pos}
        for direction in self._directions(maze, pos):
            dx, dy = direction.offset
            neighbor = (pos[0] + dx, pos[1] + dy)
            seen.add(neighbor)
            queue.append((neighbor, direction))
        while queue:
            tile, first = queue.popleft()
            if tile == self._spawn:
                return first
            for direction in self._directions(maze, tile):
                dx, dy = direction.offset
                neighbor = (tile[0] + dx, tile[1] + dy)
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append((neighbor, first))
        return Direction.NONE

    def _respawn(self) -> None:
        """Wait on the spawn tile before rejoining the shared phase."""
        self.reset_position(*self._spawn)
        self._override = GhostState.RESPAWNING
        self._respawn_left = 5.0

    def _move(self, duration: float, maze: Maze) -> None:
        """Move for duration seconds, turning only at tile centers."""
        remaining = duration
        while remaining > 1e-9 and self.speed > 0:
            if (math.isclose(self._x, round(self._x), abs_tol=1e-9) and
                    math.isclose(self._y, round(self._y), abs_tol=1e-9)):
                self._x = float(round(self._x))
                self._y = float(round(self._y))
                if self.state == GhostState.EATEN and self.pos == self._spawn:
                    self._respawn()
                    return
                self._direction = self._choosers[self.state](maze, self.pos)
                if self._direction == Direction.NONE:
                    if self.state == GhostState.EATEN:
                        self._respawn()
                    return
            dx, dy = self._direction.offset
            coordinate = self._x if dx else self._y
            sign = dx or dy
            if sign > 0:
                next_center = math.floor(coordinate + 1e-9) + 1
            else:
                next_center = math.ceil(coordinate - 1e-9) - 1
            step = min(abs(next_center - coordinate), remaining * self.speed)
            self._x += dx * step
            self._y += dy * step
            remaining -= step / self.speed

    def update(self, dt: float, maze: Maze) -> None:
        """Run the respawn wait or move through maze for dt seconds."""
        if dt <= 0:
            return
        if (self._override == GhostState.FRIGHTENED and
                not self._schedule.frightened):
            self._override = None
        if self._override == GhostState.RESPAWNING:
            self._respawn_left -= dt
            if self._respawn_left <= 0:
                self._override = None
            return
        self._move(dt, maze)
