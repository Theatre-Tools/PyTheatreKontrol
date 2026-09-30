from enum import Enum
from typing import Protocol

from pytk.protocols.power import PowerControl


class _powerState(Enum):
    """A class that represents the power state of a projector."""
    ON = "on"
    OFF = "off"
    COOLING = "cooling"
    HEATING = "heating"
    UNKNOWN = "unknown"

class ProjectorPowerControl(PowerControl, Protocol):
    """A protocol for controlling the power state of a projector."""

    def cool(self) -> None:
        """Put the projector into cooling mode."""
        ...
