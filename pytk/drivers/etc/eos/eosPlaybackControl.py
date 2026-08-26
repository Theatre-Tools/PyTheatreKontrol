from typing import TYPE_CHECKING
from pyosc import OSCMessage, OSCFloat

from pytk.lighting.playbackControl import playbackControl

if TYPE_CHECKING:
    from .eos import Eos


class EosPlaybackControl(playbackControl):
    """A class that implements the PlaybackControl protocol for Eos devices."""

    def __init__(self, _eos: Eos):
        self._eos = _eos

    async def go(self, cue: int | float | None = None) -> None:
        """Fire the next cue in the active cue list unless a cue is provided

        Args:
            cue (int | float | None, optional): Cue to fire. Defaults to None.
        """
        if not cue:
            # Fire the next cue in the active cue list
            self._eos.conn.send_message(OSCMessage(address="/eos/cues/fire", args=()))
        else:
            # Fire a specific cue
            self._eos.conn.send_message(OSCMessage(address="/eos/cues/fire", args=(OSCFloat(value=cue),)))

    async def stop(self) -> None:
        """Stop the transition of the current cue or go back to the previous cue."""
        self._eos.conn.send_message(OSCMessage(address="/eos/cues/stop", args=()))