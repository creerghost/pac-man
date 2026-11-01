"""Application entry point for Pac-Man."""

import sys

from app.core import GameEngine, Transition
from app.core.scene_manager import SceneManager
from app.io.config import GameConfig
from app.platform_pygame import PygamePlatform


def main() -> None:
    """Initialize platform, scenes, engine, and run the game loop."""
    config_file = sys.argv[1] if len(sys.argv) > 1 else "config.json"
    config = GameConfig.from_file(config_file)

    width = 800
    height = 600
    target_fps = 60

    platform = PygamePlatform(width=width, height=height, title="Pac-Man")
    scene_manager = SceneManager(start=Transition.START_GAME, config=config)
    engine = GameEngine(
        platform=platform,
        scene_manager=scene_manager,
        target_fps=target_fps,
    )

    engine.run()


if __name__ == "__main__":
    main()
