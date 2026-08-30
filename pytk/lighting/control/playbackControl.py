from typing import Optional, Protocol


class playbackControl(Protocol):
    """A protocol for controlling the playback state of a device."""

    async def go(self, cue: Optional[int | float] = None) -> None:
        """Fire the next cue, or a specific cue if provided."""
        ...

    async def stop(self) -> None:
        """Stop transition of the current cue, or go back to the previous cue."""
        ...

    async def goto_cue(self, cue: str) -> None:
        """Go to a specific cue."""
        ...
