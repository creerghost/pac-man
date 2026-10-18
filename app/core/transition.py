from enum import Enum, auto


class Transition(Enum):
    NONE = auto()
    START_GAME = auto()
    OPEN_HIGHSCORES = auto()
    OPEN_INSTRUCTIONS = auto()
    BACK_TO_MENU = auto()
    VICTORY = auto()
    GAME_OVER = auto()
    EXIT_APP = auto()
