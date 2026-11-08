"""Final score entry, saving, and platform text input."""

from pathlib import Path
from unittest.mock import Mock

import pygame
import pytest

from app.core import Color, Command, Transition, UI
from app.io import GameConfig, HighscoreRepository
from app.platform_pygame.platform import PygamePlatform
from app.scenes.final_scene import BaseFinalScene


def test_score_entry_and_submission(tmp_path: Path) -> None:
    path = tmp_path / "scores.json"
    scene = BaseFinalScene(GameConfig(highscore_filename=str(path)))
    scene.on_enter(123)
    scene.handle_command(Command.CONFIRM)
    assert scene.update(0) == (Transition.NONE, None)
    assert not path.exists()

    scene.handle_text("a!éBC123456789")
    assert scene.name == "aBC1234567"
    scene.handle_command(Command.DELETE)
    scene.handle_text("Z")
    scene.handle_command(Command.CONFIRM)
    scene.handle_command(Command.CONFIRM)
    assert scene.update(0) == (Transition.BACK_TO_MENU, None)
    assert scene.update(0) == (Transition.NONE, None)
    records = HighscoreRepository(str(path)).read_all()
    assert [(r.nickname, r.score) for r in records] == [("aBC123456Z", 123)]


def test_scene_resets_and_validates_score() -> None:
    scene = BaseFinalScene(GameConfig())
    scene.on_enter(10)
    scene.handle_text("abc")
    scene.on_enter(20)
    assert scene.name == "" and scene.score == 20
    for value in (None, True, -1, "20"):
        with pytest.raises(ValueError):
            scene.on_enter(value)


def test_final_screen_displays_score_and_name() -> None:
    scene = BaseFinalScene(GameConfig())
    scene.on_enter(42)
    scene.handle_text("Pac")
    canvas = Mock()
    canvas.ui = UI()
    scene.render(canvas)
    canvas.mlx_clear_window.assert_called_once_with(Color.BLACK)
    text = [call.args[3] for call in canvas.mlx_string_put.call_args_list]
    assert "SCORE: 42" in text and "Pac_" in text


def test_platform_preserves_input_order(
        monkeypatch: pytest.MonkeyPatch) -> None:
    events = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a, unicode="a"),
              pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE,
                                 unicode="\b"),
              pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN,
                                 unicode="\r")]
    monkeypatch.setattr(pygame.event, "get", lambda: events)
    quit_requested, inputs = PygamePlatform().poll_commands()
    assert not quit_requested
    assert inputs == [Command.LEFT, "a", Command.DELETE, Command.CONFIRM]
