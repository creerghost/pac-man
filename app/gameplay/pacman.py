from .movable_entity import MovableEntity
from .direction import Direction
from typing import Tuple
from .maze import Maze


class Pacman(MovableEntity):
    def __init__(self, pos: Tuple[float, float], speed: float):
        super().__init__(pos, speed)
        self._desired_direction = Direction.NONE

    def reset_position(self, x: float, y: float) -> None:
        super().reset_position(x, y)
        self._desired_direction = Direction.NONE

    def set_desired_direction(self, direction: Direction) -> None:
        self._desired_direction = direction

    def _handle_direction_change(self, maze: Maze) -> None:
        # same or nothing
        if (self._desired_direction == self._direction or
                self._desired_direction == Direction.NONE):
            return

        # opposite
        if (self._desired_direction == self._direction.opposite):
            self._direction = self._desired_direction
            return

        # cornering
        tx, ty = self.pos

        tolerance = 0.35
        can_turn = (
            (self._direction in (Direction.LEFT, Direction.RIGHT) and
                abs(self._x - tx) <= tolerance)
            or (self._direction in (Direction.UP, Direction.DOWN) and
                abs(self._y - ty) <= tolerance)
            or self._direction == Direction.NONE
        )

        if can_turn:
            dx, dy = self._desired_direction.offset
            target_x, target_y = tx + dx, ty + dy
            if maze.is_walkable(target_x, target_y):
                self._x = float(tx)
                self._y = float(ty)
                self.snap_to_corridor(self._desired_direction)
                self._direction = self._desired_direction

    def _move(self, dt: float, maze: Maze) -> None:
        if self._direction == Direction.NONE:
            return

        step = dt * self._speed
        tx, ty = self.pos
        dx, dy = self._direction.offset
        wall_ahead = not maze.is_walkable(tx + dx, ty + dy)

        axis_coord = self._x if dx != 0 else self._y
        axis_center = float(tx if dx != 0 else ty)
        axis_dir = dx if dx != 0 else dy

        new_coord = axis_coord + axis_dir * step

        if wall_ahead and (new_coord - axis_center) * axis_dir >= 0:
            new_coord = axis_center
            self._direction = Direction.NONE

        if dx != 0:
            self._x = new_coord
        else:
            self._y = new_coord

    def update(self, dt: float, maze: Maze) -> None:
        if dt <= 0:
            return
        self._handle_direction_change(maze)
        self._move(dt, maze)
