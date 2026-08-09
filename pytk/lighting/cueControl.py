from typing import Protocol


class cueControl(Protocol):
    """A protocol for controlling the cue state of a device."""

    async def goto_cue(self, cue: str) -> None:
        """Go to a specific cue."""
        ...

    async def record_cue(self, cue: str) -> None:
        """Record a specific cue."""
        ...

    async def delete_cue(self, cue: str) -> None:
        """Delete a specific cue."""
        ...

    async def update_cue(self, cue: str) -> None:
        """Update a specific cue."""
        ...
