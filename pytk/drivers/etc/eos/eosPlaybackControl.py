from typing import TYPE_CHECKING

from pyosc import OSCArgTypes, OSCMessage

from pytk.lighting.control.playbackControl import playbackControl

if TYPE_CHECKING:
    from .eos import Eos


class EosPlaybackControl(playbackControl):
    """A class that implements the PlaybackControl protocol for Eos devices."""

    def __init__(self, _eos: Eos):
        self._eos = _eos

    def go(self) -> None:
        """Fire the next cue in the active cue list"""
        self._eos.conn.send_message(OSCMessage(address="/eos/cues/fire", args=()))

    def stop(self) -> None:
        """Stop the transition of the current cue or go back to the previous cue."""
        self._eos.conn.send_message(OSCMessage(address="/eos/cues/stop", args=()))

    def goto_cue(self, cue: int | float) -> None:
        """Go to a specific cue."""
        if isinstance(cue, float):
            arg = OSCArgTypes.OSCFloat(value=cue)
        else:
            arg = OSCArgTypes.OSCInt(value=cue)
        self._eos.conn.send_message(OSCMessage(address="/eos/cues/fire", args=(arg,)))
