from typing import Callable, Any

from .canvas import Canvas
from .command import Command
from .transition import Transition
from .scene import Scene


class SceneManager:
    def __init__(self, start: Transition,
                 routes: dict[Transition, Callable[[], Scene]]) -> None:
        self._routes = routes
        self.should_quit = False
        self._current_scene: Scene = routes[start]()
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
                self._current_scene = self._routes[transition]()
                self._current_scene.on_enter(payload)
