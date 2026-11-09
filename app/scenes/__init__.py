"""Application scenes."""

from .final_scene import BaseFinalScene
from .game_over_scene import GameOverScene
from .highscores_scene import HighscoresScene
from .instructions_scene import InstructionsScene
from .main_menu_scene import MainMenuScene
from .victory_scene import VictoryScene
from .gameplay_scene import GameplayScene

__all__ = ["BaseFinalScene", "GameOverScene", "HighscoresScene",
           "InstructionsScene", "MainMenuScene", "VictoryScene",
           "GameplayScene"]
