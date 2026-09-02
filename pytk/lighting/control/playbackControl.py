from typing import Protocol


class playbackControl(Protocol):
    """A protocol for controlling the playback state of a device."""

    def go(self) -> None:
        """Fire the next cue"""
        ...

    def stop(self) -> None:
        """Stop transition of the current cue, or go back to the previous cue."""
        ...

    def goto_cue(self, cue: int | float) -> None:
        """Go to a specific cue."""
        ...
