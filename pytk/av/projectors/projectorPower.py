from enum import Enum

from pytk.protocols.power import PowerControl


class _powerState(Enum):
    """A class that represents the power state of a projector."""

    ON = "on"
    OFF = "off"
    COOLING = "cooling"
    HEATING = "heating"
    UNKNOWN = "unknown"


class ProjectorPowerControl(PowerControl):
    """A protocol for controlling the power state of a projector."""

    def __init__(self, projector):
        self.projector = projector

    def power_on(self) -> None:
        """Turn the projector on."""
        self.projector._driver.poweron()

    def power_off(self) -> None:
        """Turn the projector off."""
        self.projector._driver.poweroff()

    def cool(self) -> None:
        """Put the projector into cooling mode."""
        self.projector._driver.cool()

    def get_power_state(self) -> _powerState:
        """Get the current power state of the projector."""
        return self.projector._driver.get_raw_power_state()
