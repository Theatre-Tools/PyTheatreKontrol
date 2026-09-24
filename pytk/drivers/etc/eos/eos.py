from pyosc import OSCMessage, call_handler
from pyosc.types import OSCString

from pytk.core.device import Device
from pytk.core.exceptions import DeviceOfflineError, DriverError
from pytk.drivers.etc.eos.eosExceptions import EosSyntaxError
from pytk.lighting.control.cueControl import cueControl
from pytk.transport import OSC

from .eosAbout import eosAbout
from .eosAboutHandler import eosAboutHandler, register_about_handlers
from .eosDeskControls import cmdValidator, eosDeskControls
from .eosEvents import eosEvents
from .eosEventValidators import eosStates
from .eosPlaybackControl import eosPlaybackControl
from .eosPlaybackHandler import eosPlaybackHandler, register_playback_handlers, register_state_handlers
from .eosPlaybackTypes import (
    eosPlaybackStates,
)
from .eventDefenitions import Events


class Eos(Device):
    """A device that implements the Eos protocol."""

    def __init__(self, transport: OSC, device_id: str, name: str = "Eos"):
        super().__init__(device_id=device_id, name=name)
        self.conn = transport.peer()
        self.call_handler = call_handler.CallHandler(self.conn)
        self.cues = eosPlaybackControl(self)
        self.setup = eosDeskControls(self)
        self.playback = eosPlaybackStates()
        self.playback_handler = eosPlaybackHandler(self)
        self.events = eosEvents(self)
        self.event_types = Events()
        self.about = eosAbout()
        self._about_handler = eosAboutHandler(self)
        self.state: eosStates | None = None

    def connect(self) -> None:
        """Connect to the Eos device."""
        register_playback_handlers(self)
        register_about_handlers(self)
        register_state_handlers(self)

        try:
            self.conn.start_listening()
        except Exception as e:
            raise DeviceOfflineError(f"Failed to connect to Eos device: {e}")

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

    def goto_cue(self, cue: str) -> None:
        """Go to a specific cue."""
        self._eos.conn.send_message(OSCMessage(address=f"/eos/cues/{cue}/fire", args=()))

    def record_cue(self, cue: str) -> None:
        """Record a specific cue."""
        self._eos.conn.send_message(OSCMessage(address="/eos/cmd", args=(OSCString(value=f"Record Cue {cue}"),)))
