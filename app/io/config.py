import json
import os
import re
from typing import Any
from pydantic import BaseModel, ConfigDict, Field, field_validator


class LevelConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")

    width: int = 19
    height: int = 21

    @field_validator("width", "height", mode="before")
    @classmethod
    def clamp_dimension(cls, v: Any) -> int:
        try:
            val = int(v)
            if val < 5:
                print(
                    f"[Config Warning] Dimension must be >= 5 (got {v}). "
                    "Clamped to 19."
                )
                return 19
            return min(val, 99)
        except (ValueError, TypeError):
            print(
                f"[Config Warning] Invalid dimension: {v}. Using default 19."
            )
            return 19

    def __str__(self) -> str:
        return f"{self.width}x{self.height}"


class GameConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")

    highscore_filename: str = "highscores.json"
    lives: int = 3
    level_max_time: int = 90
    seed: int = 42
    pacgum: int = 42
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    levels: list[LevelConfig] = Field(default_factory=lambda: [LevelConfig()])

    @field_validator("lives", mode="before")
    @classmethod
    def clamp_lives(cls, v: Any) -> int:
        try:
            val = int(v)
            if val <= 0:
                print(
                    f"[Config Warning] 'lives' must be > 0 (got {v}). "
                    "Clamped to 3."
                )
                return 3
            return min(val, 99)
        except (ValueError, TypeError):
            print(f"[Config Warning] Invalid 'lives': {v}. Using default 3.")
            return 3

    @field_validator("level_max_time", mode="before")
    @classmethod
    def clamp_time(cls, v: Any) -> int:
        try:
            val = int(v)
            if val <= 0:
                print(
                    "[Config Warning] 'level_max_time' must be > 0. "
                    "Clamped to 90."
                )
                return 90
            return val
        except (ValueError, TypeError):
            print(
                f"[Config Warning] Invalid 'level_max_time': {v}. "
                "Using default 90."
            )
            return 90

    @field_validator(
        "points_per_pacgum",
        "points_per_super_pacgum",
        "points_per_ghost",
        mode="before",
    )
    @classmethod
    def clamp_points(cls, v: Any) -> int:
        try:
            val = int(v)
            return max(0, val)
        except (ValueError, TypeError):
            return 10

    @classmethod
    def from_file(cls, filepath: str) -> "GameConfig":
        return ConfigLoader().load(filepath)

    def __str__(self) -> str:
        levels_repr = ", ".join(
            f"{lvl.width}x{lvl.height}" for lvl in self.levels
        )
        return (
            "GameConfig(\n"
            f"  lives={self.lives},\n"
            f"  level_max_time={self.level_max_time},\n"
            f"  seed={self.seed},\n"
            f"  pacgum={self.pacgum},\n"
            f"  points=(pacgum: {self.points_per_pacgum}, "
            f"super: {self.points_per_super_pacgum}, "
            f"ghost: {self.points_per_ghost}),\n"
            f"  highscore_filename='{self.highscore_filename}',\n"
            f"  levels=[{levels_repr}]\n"
            ")"
        )


class ConfigLoader:
    def __init__(
        self, comment_prefixes: tuple[str, ...] = ("#", "//")
    ) -> None:
        self._comment_prefixes = comment_prefixes

    def _strip_comments(self, raw_text: str) -> str:
        text = re.sub(r"/\*.*?\*/", "", raw_text, flags=re.DOTALL)
        cleaned_lines: list[str] = []
        for line in text.splitlines():
            stripped = line.strip()
            if any(
                stripped.startswith(p) for p in self._comment_prefixes
            ):
                continue
            cleaned_lines.append(line)
        return "\n".join(cleaned_lines)

    def load(self, filepath: str) -> GameConfig:
        if not os.path.exists(filepath):
            print(
                f"[Config Error] '{filepath}' not found. Using safe defaults."
            )
            return GameConfig()

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                raw_text = f.read()

            clean_json = self._strip_comments(raw_text)
            data = json.loads(clean_json)

            if not isinstance(data, dict):
                print(
                    "[Config Error] Root must be JSON object in "
                    f"'{filepath}'. Using defaults."
                )
                return GameConfig()

            return GameConfig.model_validate(data)

        except json.JSONDecodeError as err:
            print(
                f"[Config Error] JSON syntax error in '{filepath}': {err}. "
                "Using defaults."
            )
            return GameConfig()
        except Exception as err:
            print(
                f"[Config Error] Unexpected error loading '{filepath}' "
                f"({err}). Using defaults."
            )
            return GameConfig()
