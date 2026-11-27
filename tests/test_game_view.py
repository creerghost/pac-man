"""Checks for drawing gameplay using the shared UI and game state."""

from typing import cast
from unittest.mock import Mock, call

import pytest

from app.core.canvas import Canvas
from app.core.ui import Color, UI
from app.gameplay.direction import Direction
from app.gameplay.game_state import GameState
from app.gameplay.game_view import GameView
from app.gameplay.ghosts import GhostState
from app.gameplay.maze import Maze
from app.gameplay.tile import Tile


def make_game(tiles: list[list[Tile]]) -> GameState:
    maze = Mock(spec=Maze)
    maze.width = len(tiles[0])
    maze.height = len(tiles)
    maze.forty_two_tiles = set()
    maze.tile_at.side_effect = lambda x, y: tiles[y][x]
    game = Mock(spec=GameState)
    game.maze = maze
    game.pacman = Mock(x=1.0, y=0.0, facing_direction=Direction.RIGHT)
    game.animation_time = 0.0
    game.death_progress = None
    game.ghosts = ()
    game.score, game.lives, game.remaining_time, game.level = 120, 2, 10.2, 4
    return cast(GameState, game)


def test_draws_state_with_shared_layout_and_palette() -> None:
    game = make_game([[Tile.WALL, Tile.PACGUM, Tile.SUPER_PACGUM, Tile.EMPTY]])
    canvas = Mock(spec=Canvas)
    canvas.ui = UI()
    size, x, y = canvas.ui.maze_layout(4, 1)

    GameView().render(canvas, game)

    canvas.mlx_clear_window.assert_called_once_with(Color.BLACK)
    assert canvas.draw_circle.call_args_list == [
        call(x + size + size // 2, y + size // 2, size // 10, Color.WHITE),
        call(x + 2 * size + size // 2, y + size // 2, size // 4, Color.WHITE),
    ]
    assert canvas.draw_sprite.call_args.args[1:] == (
        (0, 90, 543, 543), (x + size, y, size, size), 0)
    canvas.mlx_string_put.assert_called_once_with(
        canvas.ui.margin_x, 20, Color.WHITE,
        "SCORE: 120   LIVES: 2   TIME: 11   LEVEL: 4")


def test_ghosts_follow_positions_and_state() -> None:
    game = make_game([[Tile.EMPTY] * 4])
    game.ghosts = (Mock(x=0.0, y=0.0, state=GhostState.CHASE),
                   Mock(x=1.0, y=0.0, state=GhostState.FRIGHTENED),
                   Mock(x=2.0, y=0.0, state=GhostState.EATEN))
    canvas = Mock(spec=Canvas)
    canvas.ui = UI()
    GameView().render(canvas, game)
    assert [c.args[1] for c in canvas.draw_sprite.call_args_list] == [
        (0, 90, 543, 543), (0, 170, 362, 362),
        (1448, 170, 362, 362), (1810, 170, 362, 362)]


def test_death_and_direction_frames() -> None:
    game = make_game([[Tile.EMPTY] * 4])
    canvas = Mock(spec=Canvas)
    canvas.ui = UI()
    view = GameView()
    game.pacman.facing_direction = Direction.UP
    game.animation_time = 0.25
    view.render(canvas, game)
    assert canvas.draw_sprite.call_args.args[1] == (1086, 90, 543, 543)
    assert canvas.draw_sprite.call_args.args[3] == 90
    game.death_progress = 0.7
    view.render(canvas, game)
    assert canvas.draw_sprite.call_args.args[1] == (1086, 170, 362, 362)
    assert canvas.load_texture.call_count == 2


def test_invalid_maze_is_rejected() -> None:
    canvas = Mock(spec=Canvas)
    canvas.ui = UI()
    with pytest.raises(ValueError, match="dimensions"):
        GameView().render(canvas, make_game([[]]))


def test_oversized_maze_is_rejected() -> None:
    canvas = Mock(spec=Canvas)
    canvas.ui = UI()
    with pytest.raises(ValueError, match="too small"):
        GameView().render(canvas, make_game([[Tile.EMPTY] * 1000]))
