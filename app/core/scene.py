from abc import ABC, abstractmethod
from typing import Any

from .command import Command
from .transition import Transition
from .canvas import Canvas
from app.io import GameConfig


class Scene(ABC):
    def __init__(self, config: GameConfig) -> None:
        self.config = config

    @abstractmethod
    def on_enter(self, payload: Any) -> None:
        pass

    @abstractmethod
    def on_exit(self) -> None:
        pass

    @abstractmethod
    def handle_command(self, command: Command) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> tuple[Transition, Any]:
        pass

    @abstractmethod
    def render(self, canvas: Canvas) -> None:
        pass
