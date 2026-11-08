"""Game-over screen shown when the game ends."""

from .final_scene import BaseFinalScene


class GameOverScene(BaseFinalScene):
    """Show the final score and collect the player's name."""

    heading = "GAME OVER"
