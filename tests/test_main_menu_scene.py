"""Menu navigation and scene routing."""

from unittest.mock import Mock

import pytest

from app.core import Command, SceneManager, Transition, UI
from app.io import GameConfig
from app.scenes import HighscoresScene, InstructionsScene, MainMenuScene
from app.scenes.main_menu_scene import MainMenuScene as Menu


@pytest.mark.parametrize("steps,expected", [
    (0, Transition.START_GAME),
    (1, Transition.OPEN_HIGHSCORES),
    (2, Transition.OPEN_INSTRUCTIONS),
    (3, Transition.EXIT_APP),
    (4, Transition.START_GAME),
])
def test_menu_selects_destination(steps: int, expected: Transition) -> None:
    scene = Menu(GameConfig())
    scene.on_enter(None)
    for _ in range(steps):
        scene.handle_command(Command.DOWN)
    scene.handle_command(Command.CONFIRM)
    assert scene.update(0) == (expected, None)
    assert scene.update(0) == (Transition.NONE, None)


def test_up_wraps_and_selection_is_visible() -> None:
    scene = Menu(GameConfig())
    scene.handle_command(Command.UP)
    canvas = Mock()
    canvas.ui = UI()
    scene.render(canvas)
    lines = [call.args[3] for call in canvas.mlx_string_put.call_args_list]
    assert "> EXIT <" in lines
    assert Menu._team_name in lines
    scene.handle_command(Command.CONFIRM)
    assert scene.update(0) == (Transition.EXIT_APP, None)


@pytest.mark.parametrize("steps,scene_type", [
    (1, HighscoresScene), (2, InstructionsScene),
])
def test_menu_routes_and_returns(steps: int, scene_type: type) -> None:
    manager = SceneManager(Transition.BACK_TO_MENU, GameConfig())
    for _ in range(steps):
        manager.handle_command(Command.DOWN)
    manager.handle_command(Command.CONFIRM)
    manager.update(0)
    assert isinstance(manager._current_scene, scene_type)
    manager.handle_command(Command.CANCEL)
    manager.update(0)
    assert isinstance(manager._current_scene, MainMenuScene)


def test_exit_requests_engine_shutdown() -> None:
    manager = SceneManager(Transition.BACK_TO_MENU, GameConfig())
    manager.handle_command(Command.UP)
    manager.handle_command(Command.CONFIRM)
    manager.update(0)
    assert manager.should_quit
