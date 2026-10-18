from typing import Optional
import pygame

from app.core import Canvas, Command, Platform
from .canvas import PygameCanvas


class PygamePlatform(Platform):
    def __init__(self, width: int, height: int,
                 title: str = "Pac-Man") -> None:
        self._width = width
        self._height = height
        self._title = title

        self._screen: Optional[pygame.Surface] = None
        self._clock: Optional[pygame.time.Clock] = None
        self._canvas: Optional[PygameCanvas] = None

    def initialize(self) -> None:
        pygame.init()
        self._screen = pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption(self._title)
        self._clock = pygame.time.Clock()
        self._canvas = PygameCanvas(self._screen)

    def _map_key_to_command(self, key: int) -> Optional[Command]:
        match key:
            case pygame.K_UP | pygame.K_w:
                return Command.UP
            case pygame.K_DOWN | pygame.K_s:
                return Command.DOWN
            case pygame.K_LEFT | pygame.K_a:
                return Command.LEFT
            case pygame.K_RIGHT | pygame.K_d:
                return Command.RIGHT
            case pygame.K_RETURN | pygame.K_SPACE:
                return Command.CONFIRM
            case pygame.K_ESCAPE:
                return Command.CANCEL
            case pygame.K_p:
                return Command.PAUSE
            case pygame.K_BACKSPACE:
                return Command.DELETE
            case pygame.K_c:
                return Command.TOGGLE_CHEAT
            case pygame.K_1:
                return Command.CHEAT_INVINCIBLE
            case pygame.K_2:
                return Command.CHEAT_SKIP_LEVEL
            case pygame.K_3:
                return Command.CHEAT_FREEZE
            case pygame.K_4:
                return Command.CHEAT_LIFE
            case pygame.K_5:
                return Command.CHEAT_SPEED
            case _:
                return None

    def poll_commands(self) -> tuple[bool, list[Command]]:
        should_quit = False
        commands: list[Command] = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_quit = True
            elif event.type == pygame.KEYDOWN:
                cmd = self._map_key_to_command(event.key)
                if cmd is not None:
                    commands.append(cmd)

        return should_quit, commands

    def tick(self, target_fps: int) -> float:
        if self._clock is None:
            raise RuntimeError(
                "Platform not initialized. Call initialize() first."
            )
        return float(self._clock.tick(target_fps)) / 1000.0

    def get_canvas(self) -> Canvas:
        if self._canvas is None:
            raise RuntimeError(
                "Platform not initialized. Call initialize() first."
            )
        return self._canvas

    def present(self) -> None:
        pygame.display.flip()

    def shutdown(self) -> None:
        pygame.quit()
        self._screen = None
        self._clock = None
        self._canvas = None
