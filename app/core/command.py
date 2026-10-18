from enum import Enum, auto


class Command(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    CONFIRM = auto()
    CANCEL = auto()
    PAUSE = auto()
    DELETE = auto()
    TOGGLE_CHEAT = auto()
    CHEAT_INVINCIBLE = auto()
    CHEAT_SKIP_LEVEL = auto()
    CHEAT_FREEZE = auto()
    CHEAT_LIFE = auto()
    CHEAT_SPEED = auto()
