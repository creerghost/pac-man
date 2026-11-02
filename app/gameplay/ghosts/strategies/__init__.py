"""Ghost chase targeting contracts and strategies."""

from .blinky_targeting import BlinkyTargeting
from .clyde_targeting import ClydeTargeting
from .inky_targeting import InkyTargeting
from .pinky_targeting import PinkyTargeting
from .targeting_strategy import TargetingStrategy

__all__ = ["BlinkyTargeting", "ClydeTargeting", "InkyTargeting",
           "PinkyTargeting", "TargetingStrategy"]
