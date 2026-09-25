from enum import Enum
from typing import Protocol


class PowerState(Enum):
    """The power state of a device."""

    OFF = "off"
    ON = "on"
    UNKNOWN = "unknown"


class PowerControl(Protocol):
    """A protocol for controlling the power state of a device."""

    def power_on(self) -> None:
        """Turn the device on."""
        ...

    def power_off(self) -> None:
        """Turn the device off."""
        ...

    def get_power_state(self) -> PowerState:
        """Get the current power state of the device."""
        ...
