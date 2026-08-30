from typing import Protocol


class Channel(Protocol):
    """A protocol for controlling a device's channel."""

    async def intensity(self, value: float) -> None:
        """Set the intensity of the channel."""
        ...
