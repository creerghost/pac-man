"""States of a ghost's behavior."""

from enum import Enum, auto


class GhostState(Enum):
    """The movement and collision mode of a ghost."""
    CHASE = auto()
    FRIGHTENED = auto()
    EATEN = auto()
    RESPAWNING = auto()
