from pyosc import ConnectionRole, OSCFraming, OSCMessage, OSCString, OSCTransport, Peer

from pytk.core.device import Device
from pytk.lighting.control.cueControl import cueControl
from pytk.lighting.control.playbackControl import playbackControl

from .eosPlaybackControl import EosPlaybackControl


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
