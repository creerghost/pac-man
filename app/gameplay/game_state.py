"""Core gameplay state, rules, collisions, and level progression."""

from abc import ABC, abstractmethod

from mazegenerator import MazeGenerator

from app.io.config import GameConfig
from .direction import Direction
from .ghosts import (BlinkyTargeting, ClydeTargeting, Ghost, GhostGroup,
                     GhostState, InkyTargeting, PinkyTargeting)
from .maze import Maze
from .maze_adapter import MazeAdapter
from .pacman import Pacman
from .tile import Tile


class DamageHandler(ABC):
    """Strategy interface for handling dangerous ghost collisions."""

    @abstractmethod
    def handle_hit(self, game: "GameState") -> None:
        """Apply collision effect to the given game state."""
        pass


class NormalDamageHandler(DamageHandler):
    """Standard rule: Pac-Man loses a life and respawns or game ends."""

    def handle_hit(self, game: "GameState") -> None:
        """Kill Pac-Man when hit by an active ghost."""
        game.kill_pacman()


class InvincibleDamageHandler(DamageHandler):
    """Cheat rule: dangerous ghost collisions are ignored."""

    def handle_hit(self, game: "GameState") -> None:
        """Ignore ghost collision while invincibility cheat is active."""
        pass


class GameState:
    """Coordinate the maze, Pac-Man, ghosts, score, lives, and level rules."""

    _death_pause = 1.0
    _ghost_eaten_pause = 0.5

    def __init__(self, config: GameConfig, pacman_speed: float = 7.0,
                 ghost_speed: float = 6.0) -> None:
        """Initialize a new game session from configuration."""
        self._config = config
        self._pacman_speed = pacman_speed
        self._ghost_speed = ghost_speed

        self.score: int = 0
        self.lives: int = config.lives
        self.level: int = 1
        self.remaining_time: float = float(config.level_max_time)
        self.is_game_over: bool = False
        self.is_victory: bool = False

        self.damage_handler: DamageHandler = NormalDamageHandler()
        self.ghosts_frozen: bool = False
        self._speed_multiplier: float = 1.0
        self.animation_time = 0.0
        self._pause_left = 0.0
        self._death_pending = False

        self.maze: Maze = self._build_level_maze(self.level)
        self.pacman: Pacman = self._create_pacman()
        self.ghost_group: GhostGroup = self._create_ghosts()

    @property
    def ghosts(self) -> tuple[Ghost, ...]:
        """Return all ghosts in creation order."""
        return self.ghost_group.ghosts

    @property
    def is_invincible(self) -> bool:
        """Return True if the invincibility cheat is active."""
        return isinstance(self.damage_handler, InvincibleDamageHandler)

    @property
    def is_speed_boosted(self) -> bool:
        """Return True if the speed boost cheat is active."""
        return self._speed_multiplier > 1.0

    def set_direction(self, direction: Direction) -> None:
        """Buffer the player's desired movement direction."""
        self.pacman.set_desired_direction(direction)

    def update(self, dt: float) -> None:
        """Advance the gameplay simulation by dt seconds."""
        if dt <= 0 or self.is_game_over or self.is_victory:
            return

        self.animation_time += dt
        dt = self._update_pause(dt)
        if dt > 0 and not self.is_game_over:
            self.remaining_time -= dt
            if self.remaining_time <= 0:
                self.remaining_time = 0.0
                self.is_game_over = True
                return
            self._update_movement(dt)

    def _update_pause(self, dt: float) -> float:
        """Advance an active pause and return time available for gameplay."""
        if self._pause_left > 0:
            paused = min(dt, self._pause_left)
            self._pause_left -= paused
            dt -= paused
            if self._pause_left > 1e-9:
                return 0.0
            self._pause_left = 0.0
            if self._death_pending:
                self._death_pending = False
                if self.lives == 0:
                    self.is_game_over = True
                    return 0.0
                self.reset_positions()
        return dt

    def _update_movement(self, dt: float) -> bool:
        """Advance movement and interactions; stop after a transition."""
        self.pacman.update(dt * self._speed_multiplier, self.maze)
        self._consume_pellet()

        if self.maze.pacgums_left() == 0:
            self.next_level()
            return False

        lives_before = self.lives
        self._check_ghost_collisions()
        if self.is_game_over or self.lives != lives_before or self._pause_left:
            return False

        if not self.ghosts_frozen:
            pac_pos = (self.pacman.x, self.pacman.y)
            self.ghost_group.update(dt, self.maze, pac_pos)
            self._check_ghost_collisions()
        return (not self.is_game_over and self.lives == lives_before
                and self._pause_left == 0)

    def kill_pacman(self) -> None:
        """Freeze at the collision before respawning or ending the game."""
        self.lives = max(0, self.lives - 1)
        self._death_pending = True
        self._pause_left = self._death_pause

    def reset_positions(self) -> None:
        """Place Pac-Man and all ghosts back on their spawn tiles."""
        spawn_x, spawn_y = self.maze.pacman_spawn
        self.pacman.reset_position(float(spawn_x), float(spawn_y))
        self.ghost_group.reset()

    def next_level(self) -> None:
        """Advance to the next level or mark the game as won."""
        self._pause_left = 0.0
        self._death_pending = False
        if self.level >= len(self._config.levels):
            self.is_victory = True
            return

        self.level += 1
        self.remaining_time = float(self._config.level_max_time)
        self.maze = self._build_level_maze(self.level)
        self.pacman = self._create_pacman()
        self.ghost_group = self._create_ghosts()

    def toggle_invincible_cheat(self) -> None:
        """Toggle the invincibility cheat mode on or off."""
        if self.is_invincible:
            self.damage_handler = NormalDamageHandler()
        else:
            self.damage_handler = InvincibleDamageHandler()

    def toggle_speed_cheat(self) -> None:
        """Toggle Pac-Man's speed boost cheat on or off."""
        self._speed_multiplier = 1.0 if self.is_speed_boosted else 2.0

    def toggle_freeze_cheat(self) -> None:
        """Toggle freezing of ghost movement and schedule."""
        self.ghosts_frozen = not self.ghosts_frozen

    def add_life_cheat(self) -> None:
        """Grant one extra life to the player."""
        self.lives += 1

    def skip_level_cheat(self) -> None:
        """Immediately complete the current level."""
        self.next_level()

    def _consume_pellet(self) -> None:
        """Eat a pacgum or super-pacgum on Pac-Man's current tile."""
        x, y = self.pacman.pos
        tile = self.maze.tile_at(x, y)
        if tile == Tile.PACGUM:
            self.maze.set_tile(x, y, Tile.EMPTY)
            self.score += self._config.points_per_pacgum
        elif tile == Tile.SUPER_PACGUM:
            self.maze.set_tile(x, y, Tile.EMPTY)
            self.score += self._config.points_per_super_pacgum
            self.ghost_group.frighten()

    def _check_ghost_collisions(self) -> None:
        """Resolve collisions between Pac-Man and any ghost on his tile."""
        pacman_tile = self.pacman.pos
        for ghost in self.ghost_group.ghosts:
            if ghost.pos != pacman_tile:
                continue
            if ghost.state == GhostState.FRIGHTENED:
                ghost.eat()
                self.score += self._config.points_per_ghost
                self._pause_left = self._ghost_eaten_pause
                break
            elif ghost.state in (GhostState.CHASE, GhostState.SCATTER):
                self.damage_handler.handle_hit(self)
                break

    def _build_level_maze(self, level: int) -> Maze:
        """Build a maze for the given 1-based level number."""
        lvl_cfg = self._config.levels[level - 1]
        seed = self._config.seed if level == 1 else 0
        size = (lvl_cfg.width, lvl_cfg.height)
        generator = MazeGenerator(size=size, perfect=False, seed=seed)
        return MazeAdapter(generator)

    def _create_pacman(self) -> Pacman:
        """Create Pac-Man at the current maze's spawn tile."""
        spawn_x, spawn_y = self.maze.pacman_spawn
        return Pacman((float(spawn_x), float(spawn_y)), self._pacman_speed)

    def _create_ghosts(self) -> GhostGroup:
        """Create the four ghosts at the maze corners with their strategies."""
        group = GhostGroup()
        spawns = self.maze.ghost_spawns
        pac_pos = (self.pacman.x, self.pacman.y)
        speed = self._ghost_speed

        blinky = group.add(spawns[0], speed, BlinkyTargeting(), pac_pos)
        pinky_strat = PinkyTargeting(lambda: self.pacman.direction)
        group.add(spawns[1], speed, pinky_strat, pac_pos)
        inky_strat = InkyTargeting(lambda: self.pacman.direction,
                                   lambda: blinky.pos)
        group.add(spawns[2], speed, inky_strat, pac_pos)
        group.add(spawns[3], speed, ClydeTargeting(spawns[3]), pac_pos)
        return group
