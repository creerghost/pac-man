"""Highscore repository for reading, writing, and updating player scores."""

import json
import os
from typing import Any
from pydantic import BaseModel, Field, ValidationError, field_validator


class HighscoreRecord(BaseModel):
    """Model representing a single player score record."""

    nickname: str = Field(
        min_length=1,
        max_length=10,
        pattern=r"^[a-zA-Z0-9 ]+$",
    )
    score: int = Field(ge=0)

    @field_validator("nickname", mode="before")
    @classmethod
    def strip_nickname(cls, v: Any) -> str:
        """Strip surrounding spaces before validation."""
        cleaned = str(v).strip()
        if not cleaned:
            raise ValueError("Nickname cannot be empty")
        return cleaned


class HighscoreRepository:
    """Handles reading, writing, and upserting player highscores in JSON."""

    MAX_RECORDS: int = 10

    def __init__(self, filepath: str = "highscores.json") -> None:
        self.filepath = filepath

    def read_all(self) -> list[HighscoreRecord]:
        """Load and return records from JSON file.

        Returns an empty list if file is missing, empty, or corrupted.
        """
        if not os.path.exists(self.filepath):
            return []

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, list):
                return []

            records: list[HighscoreRecord] = []
            for item in data:
                if not isinstance(item, dict):
                    continue
                try:
                    records.append(HighscoreRecord(**item))
                except ValidationError:
                    continue

            records.sort(key=lambda r: r.score, reverse=True)
            return records

        except Exception:
            return []

    def save(self, data: list[HighscoreRecord]) -> None:
        """Safely write records back to the JSON file."""
        try:
            dirname = os.path.dirname(self.filepath)
            if dirname:
                os.makedirs(dirname, exist_ok=True)

            with open(self.filepath, "w", encoding="utf-8") as f:
                json_data = [item.model_dump() for item in data]
                json.dump(json_data, f, indent=2)
        except OSError as e:
            print(f"[Highscore Error] Could not save highscores: {e}")

    def upsert_score(self, nickname: str, score: int) -> None:
        """Add a new score or update an existing player's record."""
        new_record = HighscoreRecord(nickname=nickname, score=score)

        records = self.read_all()

        found = False
        for item in records:
            if item.nickname.lower() == new_record.nickname.lower():
                if new_record.score > item.score:
                    item.score = new_record.score
                item.nickname = new_record.nickname
                found = True
                break

        if not found:
            records.append(new_record)

        records.sort(key=lambda r: r.score, reverse=True)
        self.save(records)
