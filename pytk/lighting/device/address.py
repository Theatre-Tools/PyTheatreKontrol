from typing import Protocol


class Address(Protocol):
    """A protocol for controlling an address."""

    async def set_level(self, level: float) -> None:
        """Set the level of the address (1-100)."""
        ...

    async def set_value(self, value: int) -> None:
        """Set the value of the address (0-255)."""
        ...
