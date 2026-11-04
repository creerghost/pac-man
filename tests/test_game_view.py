"""Checks for drawing the gameplay view through the Canvas contract."""

from typing import cast
from unittest.mock import Mock, call

import pytest
from pytest import CaptureFixture
from webcolors import name_to_rgb

from app.core.canvas import Canvas
from app.gameplay.game_view import GameView
from app.gameplay.maze import Maze
from app.gameplay.pacman import Pacman
from app.gameplay.tile import Tile
from app.io.config import GameConfig


def make_maze(tiles: list[list[Tile]]) -> Maze:
    """Create a Maze double that returns tiles from the given grid."""
    maze = Mock(spec=Maze)
    maze.width = len(tiles[0])
    maze.height = len(tiles)
    maze.tile_at.side_effect = lambda x, y: tiles[y][x]
    return cast(Maze, maze)


def test_wall_is_centered_in_space_below_hud() -> None:
    """Fit and center a non-square maze in the area below the HUD."""
    maze = make_maze([[Tile.WALL, Tile.EMPTY, Tile.EMPTY],
                      [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY]])
    canvas = Mock(spec=Canvas)
    view = GameView(200, 200, GameConfig())

    view.render(canvas, maze, Pacman((1.0, 1.0), 1.0), 0, 3, 90, 1)

    canvas.draw_rect.assert_called_once_with(
        1, 54, 66, 66, name_to_rgb("blue"))


def test_maze_and_pacman_are_drawn_at_tile_centers() -> None:
    """Draw both pellet sizes and Pac-Man, leaving empty tiles blank."""
    maze = make_maze([[Tile.WALL, Tile.PACGUM, Tile.SUPER_PACGUM, Tile.EMPTY]])
    canvas = Mock(spec=Canvas)
    view = GameView(200, 100, GameConfig())

    view.render(canvas, maze, Pacman((0.5, 0.0), 1.0), 0, 3, 90, 1)

    canvas.mlx_clear_window.assert_called_once_with(name_to_rgb("black"))
    assert canvas.draw_circle.call_args_list == [
        call(75, 70, 5, name_to_rgb("white")),
        call(125, 70, 12, name_to_rgb("white")),
        call(50, 70, 20, name_to_rgb("yellow")),
    ]
    canvas.draw_rect.assert_called_once_with(
        0, 45, 50, 50, name_to_rgb("blue"))


def test_hud_shows_current_values_each_frame() -> None:
    """Show updated values and round remaining seconds up for display."""
    maze = make_maze([[Tile.EMPTY]])
    canvas = Mock(spec=Canvas)
    pacman = Pacman((0.0, 0.0), 1.0)
    view = GameView(800, 600, GameConfig())

    view.render(canvas, maze, pacman, 120, 2, 10.2, 4)
    view.render(canvas, maze, pacman, 130, 1, 0.0, 5)

    assert canvas.mlx_string_put.call_args_list == [
        call(0, 0, name_to_rgb("white"),
             "SCORE: 120   LIVES: 2   TIME: 11   LEVEL: 4"),
        call(0, 0, name_to_rgb("white"),
             "SCORE: 130   LIVES: 1   TIME: 0   LEVEL: 5"),
    ]


@pytest.mark.parametrize("width,height", [(0, 100), (100, 40), (1, 41)])
def test_window_too_small_for_maze_raises_clear_error(
        width: int, height: int) -> None:
    """Reject a viewport that cannot fit even one pixel per tile."""
    maze = make_maze([[Tile.EMPTY, Tile.EMPTY]])
    view = GameView(width, height, GameConfig())

    with pytest.raises(ValueError, match="too small"):
        view.render(Mock(spec=Canvas), maze, Pacman((0.0, 0.0), 1.0),
                    0, 3, 90, 1)


def test_zero_width_maze_raises_clear_error() -> None:
    """Reject an empty maze before calculating a viewport."""
    view = GameView(800, 600, GameConfig())

    with pytest.raises(ValueError, match="maze dimensions"):
        view.render(Mock(spec=Canvas), make_maze([[]]),
                    Pacman((0.0, 0.0), 1.0), 0, 3, 90, 1)


def test_single_pixel_tiles_do_not_produce_negative_radii() -> None:
    """Keep circles drawable even when the maze fits at one pixel per tile."""
    canvas = Mock(spec=Canvas)
    maze = make_maze([[Tile.PACGUM, Tile.SUPER_PACGUM]])
    view = GameView(2, 41, GameConfig())

    view.render(canvas, maze, Pacman((0.0, 0.0), 1.0), 0, 3, 90, 1)

    assert canvas.draw_circle.call_args_list == [
        call(0, 40, 0, name_to_rgb("white")),
        call(1, 40, 0, name_to_rgb("white")),
        call(0, 40, 0, name_to_rgb("yellow")),
    ]


@pytest.mark.parametrize("height", [0, 19, -1, True, None, "bad", 20.5])
def test_invalid_hud_height_uses_default_with_one_warning(
        height: object, capsys: CaptureFixture[str]) -> None:
    """Use the default HUD height and warn once for an invalid value."""
    config = GameConfig.model_validate({"hud_height": height})

    assert config.hud_height == 40
    output = capsys.readouterr().out.splitlines()
    assert len(output) == 1 and "hud_height" in output[0] and "40" in output[0]


def test_missing_hud_height_uses_default_with_one_warning(
        capsys: CaptureFixture[str]) -> None:
    """Use the default HUD height and warn once when the key is missing."""
    config = GameConfig.model_validate({})

    assert config.hud_height == 40
    output = capsys.readouterr().out.splitlines()
    assert len(output) == 1 and "hud_height" in output[0] and "40" in output[0]


def test_custom_hud_height_changes_maze_offset() -> None:
    """Reserve the configured height when positioning the maze."""
    canvas = Mock(spec=Canvas)
    maze = make_maze([[Tile.WALL, Tile.EMPTY, Tile.EMPTY],
                      [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY]])
    view = GameView(200, 200, GameConfig(hud_height=60))

    view.render(canvas, maze, Pacman((1.0, 1.0), 1.0), 0, 3, 90, 1)

    canvas.draw_rect.assert_called_once_with(
        1, 64, 66, 66, name_to_rgb("blue"))


def test_hud_too_tall_for_maze_uses_default_once(
        capsys: CaptureFixture[str]) -> None:
    """Fall back to the default when the configured HUD leaves no maze room."""
    maze = make_maze([[Tile.WALL, Tile.EMPTY], [Tile.EMPTY, Tile.EMPTY]])
    canvas = Mock(spec=Canvas)
    pacman = Pacman((1.0, 1.0), 1.0)
    view = GameView(200, 100, GameConfig(hud_height=100))

    view.render(canvas, maze, pacman, 0, 3, 90, 1)
    view.render(canvas, maze, pacman, 0, 3, 90, 1)

    assert canvas.draw_rect.call_args_list == [
        call(70, 40, 30, 30, name_to_rgb("blue")),
        call(70, 40, 30, 30, name_to_rgb("blue")),
    ]
    output = capsys.readouterr().out.splitlines()
    assert len(output) == 1 and "hud_height" in output[0] and "40" in output[0]
