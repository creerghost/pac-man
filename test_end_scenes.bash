.venv/bin/python - <<'PY'
from pathlib import Path
from tempfile import TemporaryDirectory

from app.core import Command, Transition
from app.io import GameConfig
from app.platform_pygame import PygamePlatform
from app.scenes.final_scene import BaseFinalScene
from app.scenes.game_over_scene import GameOverScene
from app.scenes.victory_scene import VictoryScene

with TemporaryDirectory() as directory:
    score_file = Path(directory) / "scores.json"
    config = GameConfig(highscore_filename=str(score_file))

    for scene_type in (BaseFinalScene, VictoryScene, GameOverScene):
        scene = scene_type(config)
        scene.on_enter(1234)
        platform = PygamePlatform(title=scene_type.__name__)
        platform.initialize()
        try:
            while True:
                should_quit, inputs = platform.poll_commands()
                if should_quit:
                    break

                for item in inputs:
                    if isinstance(item, Command):
                        scene.handle_command(item)
                    else:
                        scene.handle_text(item)

                transition, _ = scene.update(platform.tick(60))
                if transition == Transition.BACK_TO_MENU:
                    print(f"Saved scores: {score_file.read_text()}")
                    break

                scene.render(platform.get_canvas())
                platform.present()
        finally:
            platform.shutdown()
PY
