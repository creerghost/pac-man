"""Pac-Man keeps facing the direction he was moving when blocked."""

from unittest.mock import Mock

import pytest

from app.gameplay.direction import Direction
from app.gameplay.maze import Maze
from app.gameplay.pacman import Pacman


@pytest.mark.parametrize(
    "direction",
    [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
)
def test_facing_survives_wall_collision(direction: Direction) -> None:
    maze = Mock(spec=Maze)
    dx, dy = direction.offset
    maze.is_walkable.side_effect = lambda x, y: (x, y) == (dx, dy)
    pacman = Pacman((0.0, 0.0), 1.0)
    pacman.set_desired_direction(direction)
    pacman.update(1.0, maze)
    pacman.update(0.1, maze)
    assert pacman.direction == Direction.NONE
    assert pacman.facing_direction == direction
    pacman.update(0.1, maze)
    assert pacman.facing_direction == direction
    pacman.reset_position(0.0, 0.0)
    assert pacman.facing_direction == Direction.RIGHT
