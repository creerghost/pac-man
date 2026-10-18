from typing import Callable, Any

from .canvas import Canvas
from .command import Command
from .transition import Transition
from .scene import Scene

from app.io import GameConfig
from app.utils.test_scene import FirstScene, SecondScene


class SceneManager:
    def __init__(self, start: Transition, config: GameConfig) -> None:
        self._config = config
        self._routes: dict[Transition, Callable[[GameConfig], Scene]] = {
            Transition.BACK_TO_MENU: FirstScene,
            Transition.START_GAME: SecondScene,
        }
        self.should_quit = False
        self._current_scene: Scene = self._routes[start](self._config)
        self._current_scene.on_enter(None)

    def handle_command(self, command: Command) -> None:
        self._current_scene.handle_command(command)

    def update(self, dt: float) -> None:
        transition, payload = self._current_scene.update(dt)
        self._route_transition(transition, payload)

    def render(self, canvas: Canvas) -> None:
        self._current_scene.render(canvas)

    def _route_transition(self, transition: Transition, payload: Any) -> None:
        match transition:
            case Transition.NONE:
                pass
            case Transition.EXIT_APP:
                self._current_scene.on_exit()
                self.should_quit = True
            case _:
                self._current_scene.on_exit()
                self._current_scene = self._routes[transition](self._config)
                self._current_scene.on_enter(payload)
