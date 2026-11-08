"""Victory screen shown after completing the game."""

from .final_scene import BaseFinalScene


class VictoryScene(BaseFinalScene):
    """Congratulate the player and collect their final score."""

    heading = "CONGRATULATIONS!"
