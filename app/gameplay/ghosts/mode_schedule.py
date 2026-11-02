"""Scatter/chase schedule and fright timer shared by all ghosts."""

from .ghost_state import GhostState


class ModeSchedule:
    """Alternate scatter and chase, pausing the cycle while frightened."""
    _NEXT = {GhostState.SCATTER: GhostState.CHASE,
             GhostState.CHASE: GhostState.SCATTER}

    def __init__(self) -> None:
        """Initialize the scatter and chase durations in seconds."""
        self._durations = {GhostState.SCATTER: 7.0, GhostState.CHASE: 20.0}
        self.reset()

    @property
    def mode(self) -> GhostState:
        """Return the current phase, SCATTER or CHASE."""
        return self._mode

    @property
    def frightened(self) -> bool:
        """Return True while the fright timer is running."""
        return self._fright_left > 0

    def reset(self) -> None:
        """Restart the cycle in scatter and cancel any fright."""
        self._mode = GhostState.SCATTER
        self._mode_left = self._durations[self._mode]
        self._fright_left = 0.0

    def frighten(self) -> None:
        """Start or refresh the fright timer."""
        self._fright_left = 6.0

    def update(self, dt: float) -> None:
        """Spend dt seconds on the fright timer first, then on the cycle."""
        fright = min(dt, self._fright_left)
        self._fright_left -= fright
        dt -= fright
        while dt > 0:
            step = min(dt, self._mode_left)
            self._mode_left -= step
            dt -= step
            if self._mode_left <= 0:
                self._mode = self._NEXT[self._mode]
                self._mode_left = self._durations[self._mode]
