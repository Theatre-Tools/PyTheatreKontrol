from typing import Protocol


class cueControl(Protocol):
    """A protocol for controlling the cue state of a device."""

    def record_cue(self, cue: str) -> None:
        """Record a specific cue."""
        ...

    def delete_cue(self, cue: str) -> None:
        """Delete a specific cue."""
        ...

    def update_cue(self, cue: str) -> None:
        """Update a specific cue."""
        ...

    def cue_time(self, cue: str, time: float) -> None:
        """Set the time of a specific cue."""
        ...

    def copy_cue(self, source_cue: str, destination_cue: str) -> None:
        """Copy a specific cue to a new cue."""
        ...

    def move_cue(self, source_cue: str, destination_cue: str) -> None:
        """Move a specific cue to a new cue."""
        ...
