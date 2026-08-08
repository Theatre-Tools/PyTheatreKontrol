from enum import Enum
from typing import Protocol


class HealthState(Enum):
    """The health state of a device."""

    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class HealthCheck(Protocol):
    """A protocol for checking the health state of a device."""

    async def check_health(self) -> HealthState:
        """Check the health state of the device."""
        ...
