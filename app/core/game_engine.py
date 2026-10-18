from .platform import Platform
from .scene_manager import SceneManager


class GameEngine:
    def __init__(self, platform: Platform, scene_manager: SceneManager,
                 target_fps: int = 60) -> None:
        self._platform = platform
        self._scene_manager = scene_manager
        self._target_fps = target_fps
        self._is_running = False

    def run(self) -> None:
        self._is_running = True
        self._platform.initialize()
        canvas = self._platform.get_canvas()

        try:
            while self._is_running and not self._scene_manager.should_quit:
                dt = self._platform.tick(self._target_fps)
                should_quit, commands = self._platform.poll_commands()
                if should_quit:
                    break
                for cmd in commands:
                    self._scene_manager.handle_command(cmd)
                self._scene_manager.update(dt)
                if self._scene_manager.should_quit:
                    break
                self._scene_manager.render(canvas)
                self._platform.present()
        finally:
            self._is_running = False
            self._platform.shutdown()
