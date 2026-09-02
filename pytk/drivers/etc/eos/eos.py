from pydantic import BaseModel
from pyosc import ConnectionRole, OSCFraming, OSCInt, OSCMessage, OSCString, OSCTransport, Peer, call_handler

from pytk.core.device import Device
from pytk.core.exceptions import DriverError
from pytk.drivers.etc.eos.eosExceptions import EosSyntaxError
from pytk.lighting.control.cueControl import cueControl

from .eosDeskControls import eosDeskControls
from .eosPlaybackControl import EosPlaybackControl
from .eosPlaybackHandler import eosPlaybackHandler
from .eosPlaybackTypes import (
    eosActiveCueCompletionValidator,
    eosActiveCueValidator,
    eosCuePendingValidator,
    eosPlaybackEventValidator,
    eosPlaybackStates,
)


class cmdValidator(BaseModel):
    """A validator for the /eos/out/cmd message."""

    address: str
    args: tuple[OSCString, OSCInt]

    @property
    def success(self) -> bool:
        """Returns True if the command was successful, False otherwise."""
        return self.args[1].value == 0

    @property
    def cmd(self) -> str:
        """Returns the command that was sent."""
        return str(self.args[0].value)


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
        self.call_handler = call_handler.CallHandler(self.conn)
        self.cues = EosPlaybackControl(self)
        self.setup = eosDeskControls(self)
        self.playback = eosPlaybackStates()
        self.eos_playback_handler = eosPlaybackHandler(self)

    def connect(self) -> None:
        """Connect to the Eos device."""
        self.conn.register_handler(
            message_address="/eos/out/active/cue/*/*",
            validator=eosActiveCueValidator,
            func=self.eos_playback_handler.handle_playback_event,
        )
        self.conn.register_handler(
            message_address="/eos/out/active/cue",
            validator=eosActiveCueCompletionValidator,
            func=self.eos_playback_handler.handle_playback_event,
        )
        self.conn.register_handler(
            message_address="/eos/out/cue/pending/*/*",
            validator=eosCuePendingValidator,
            func=self.eos_playback_handler.handle_playback_event,
        )
        self.conn.register_handler(
            message_address="/eos/out/event/cue/*/*/*",
            validator=eosPlaybackEventValidator,
            func=self.eos_playback_handler.handle_playback_event,
        )
        self.conn.start_listening()

    def disconnect(self) -> None:
        """Disconnect from the Eos device."""
        self.conn.stop_listening()

    def cmd(self, command: str) -> str | None:
        """Sends a command directly to the Eos programmer.
        Listens for a response on the `/eos/out/cmd` address, which may contain a `-` if there is a syntax error.
        """
        cmd = self.call_handler.call(
            message=OSCMessage(address="/eos/newcmd", args=(OSCString(value=command),)),
            message_return_address="/eos/out/cmd",
            validator=cmdValidator,
        )
        if not isinstance(cmd, list) and cmd:
            cmd = cmd.message
        else:
            raise DriverError(f"Unexpected response type: {type(cmd)}")
        if not cmd.success:
            raise EosSyntaxError(f"Command '{cmd.cmd}' failed with error code {cmd.args[1].value}")
        else:
            return cmd.cmd


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
