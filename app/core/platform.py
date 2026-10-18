from abc import abstractmethod, ABC
from typing import Tuple, List
from .canvas import Canvas
from .command import Command


class Platform(ABC):
    @abstractmethod
    def initialize(self) -> None:
        pass

    @abstractmethod
    def poll_commands(self) -> Tuple[bool, List[Command]]:
        pass

    @abstractmethod
    def tick(self, target_fps: int) -> float:
        pass

    @abstractmethod
    def get_canvas(self) -> Canvas:
        pass

    @abstractmethod
    def present(self) -> None:
        pass

    @abstractmethod
    def shutdown(self) -> None:
        pass
