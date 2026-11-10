"""Normal mode and fright timer shared by all ghosts."""

from .ghost_state import GhostState


class ModeSchedule:
    """Keep ghosts in chase mode and track their shared fright timer."""

    def __init__(self) -> None:
        """Initialize the fright timer."""
        self.reset()

    @property
    def mode(self) -> GhostState:
        """Return the normal chase mode."""
        return GhostState.CHASE

    @property
    def frightened(self) -> bool:
        """Return True while the fright timer is running."""
        return self._fright_left > 0

    @property
    def frightened_time_left(self) -> float:
        """Return the remaining frightened time in seconds."""
        return self._fright_left

    def reset(self) -> None:
        """Cancel any fright."""
        self._fright_left = 0.0

    def frighten(self) -> None:
        """Start or refresh the fright timer."""
        self._fright_left = 8.0

    def update(self, dt: float) -> None:
        """Advance the fright timer by dt seconds."""
        self._fright_left = max(0.0, self._fright_left - dt)
