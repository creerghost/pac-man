"""Tests for the ghosts' normal mode."""

from app.gameplay.ghosts import GhostState, ModeSchedule


def test_ghosts_chase_before_and_after_fright() -> None:
    """Normal mode stays chase as time passes and fright expires."""
    schedule = ModeSchedule()
    assert schedule.mode == GhostState.CHASE
    schedule.update(30.0)
    assert schedule.mode == GhostState.CHASE
    schedule.frighten()
    schedule.update(7.0)
    assert not schedule.frightened
    assert schedule.mode == GhostState.CHASE
    schedule.reset()
    assert schedule.mode == GhostState.CHASE
