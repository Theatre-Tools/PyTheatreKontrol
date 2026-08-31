from pyosc import ConnectionRole, OSCFraming, OSCMessage, OSCString, OSCTransport, Peer

from pytk.core.device import Device
from pytk.lighting.control.cueControl import cueControl

from .eosPlaybackControl import EosPlaybackControl
from .eosPlaybackHandler import eosPlaybackHandler
from .eosPlaybackTypes import (
    eosActiveCueCompletionValidator,
    eosActiveCueValidator,
    eosCuePendingValidator,
    eosPlaybackEventValidator,
    eosPlaybackStates,
)


class Eos(Device):
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
        self.playback = eosPlaybackStates()
        self.eos_playback_handler = eosPlaybackHandler(self)

    def connect(self) -> None:
        """Connect to the Eos device."""
        self.conn.register_handler(message_address="/eos/out/active/cue/*/*", validator=eosActiveCueValidator, func=self.eos_playback_handler.handle_playback_event)
        self.conn.register_handler(message_address="/eos/out/active/cue", validator=eosActiveCueCompletionValidator, func=self.eos_playback_handler.handle_playback_event)
        self.conn.register_handler(message_address="/eos/out/cue/pending/*/*", validator=eosCuePendingValidator, func=self.eos_playback_handler.handle_playback_event)
        self.conn.register_handler(message_address="/eos/out/event/cue/*/*/*", validator=eosPlaybackEventValidator, func=self.eos_playback_handler.handle_playback_event)
        self.conn.start_listening()

    def disconnect(self) -> None:
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
