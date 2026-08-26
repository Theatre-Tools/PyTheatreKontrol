from pyosc import ConnectionRole, OSCFloat, OSCFraming, OSCMessage, OSCString, OSCTransport, Peer

from pytk.core.device import Device
from pytk.lighting.cueControl import cueControl
from pytk.lighting.playbackControl import playbackControl


class Eos(Device, playbackControl):
    """A device that implements the Eos protocol."""

    def __init__(
        self,
        device_id: str,
        host: str,
        port: int = 3037,
        name: str = "Eos",
    ):
        super().__init__(device_id=device_id, name=name)
        self.conn = Peer(
            connection_role=ConnectionRole.INITIATING,
            transport=OSCTransport.TCP,
            remote_address=host,
            remote_port=port,
            framing=OSCFraming.OSC11,
        )
        self.cues = EosPlaybackControl(self)

    async def connect(self) -> None:
        """Connect to the Eos device."""
        self.conn.start_listening()

    async def disconnect(self) -> None:
        """Disconnect from the Eos device."""
        self.conn.stop_listening()


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


class EosCueControl(cueControl):
    """A class that implements the CueControl protocol for Eos devices."""

    def __init__(self, _eos: Eos):
        self._eos = _eos

    async def goto_cue(self, cue: str) -> None:
        """Go to a specific cue."""
        self._eos.conn.send_message(OSCMessage(address=f"/eos/cues/{cue}/fire", args=()))

    async def record_cue(self, cue: str) -> None:
        """Record a specific cue."""
        self._eos.conn.send_message(OSCMessage(address="/eos/cmd", args=(OSCString(value=f"Record Cue {cue}"),)))
