"""Instructions screen navigation and display."""

from unittest.mock import Mock

import pytest

from app.core import Command, Transition, UI
from app.io import GameConfig
from app.scenes.instructions_scene import InstructionsScene


@pytest.mark.parametrize("command", [Command.CONFIRM, Command.CANCEL])
def test_return_to_menu(command: Command) -> None:
    scene = InstructionsScene(GameConfig())
    scene.on_enter(None)
    scene.handle_command(command)
    assert scene.update(0) == (Transition.BACK_TO_MENU, None)
    assert scene.update(0) == (Transition.NONE, None)


def test_instructions_fit_and_include_controls() -> None:
    canvas = Mock()
    canvas.ui = UI()
    InstructionsScene(GameConfig()).render(canvas)
    calls = canvas.mlx_string_put.call_args_list
    lines = [call.args[3] for call in calls]
    sections = ("GOAL", "CONTROLS", "CHEAT KEYS (DEBUG)")
    assert all(section in lines for section in sections)
    assert "ARROWS / WASD: MOVE" in lines
    assert "5: SPEED BOOST" in lines
    for call in calls:
        x, y, _, text = call.args
        size = canvas.ui.font_title if text == "INSTRUCTIONS" else 16
        assert 0 <= x
        assert x + canvas.ui.text_width(text, size) <= canvas.ui.width
        assert 0 <= y and y + size <= canvas.ui.height
