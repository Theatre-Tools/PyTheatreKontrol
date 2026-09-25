
from typing import TYPE_CHECKING

from pyosc import OSCMessage
from pyosc.types import OSCFloat

from pytk.lighting.control.programmerControl import programmerControl
from pytk.lighting.device.address import Address
from pytk.lighting.device.channel import Channel

if TYPE_CHECKING:
    from .eos import Eos


class _eosChannel(Channel):
    """A class representing a channel in the Eos device.
    Currently this class has support for only intensity control, but can be extended to support other channel features in the future."""

    def __init__(self, eos: "Eos", channel_number: int):
        self._eos = eos
        self.channel_number = channel_number
    def select(self) -> None:
        """Select the channel."""
        self._eos.conn.send_message(OSCMessage(address=f"/eos/chan/{self.channel_number}", args=()))

    def intensity(self, value: float) -> None:
        """Set the intensity of the channel."""
        if not (0.0 <= value <= 100.0):
            raise ValueError("Intensity must be between 0.0 and 100.0.")
        self._eos.conn.send_message(OSCMessage(address=f"/eos/chan/{self.channel_number}", args=(OSCFloat(value=value),)))

    def flash(self) -> None:
        """Flash the channel."""
        ## Some of the implemtentation is borked so we bypass that with cmd
        #self._eos.cmd(f'Chan {self.channel_number} Flash #')
        self.select()
        self._eos.keys.send_key("Flash", button_edge=False)

class _eosAddress(Address):
    """A class representing an ABSOLUTE (e.g. 513 = universe 2 address 1) address in the Eos device.
    Currently this class has support for only level and value control, but can be extended to support other address features in the future."""

    def __init__(self, eos: "Eos", address_number: int):
        self._eos = eos
        self.address_number = address_number

    def type(self) -> None:
        """Type the address in the eos Console."""
        self._eos.conn.send_message(OSCMessage(address=f"/eos/addr/{self.address_number}", args=()))

    def set_level(self, level: float) -> None:
        """Set the level of the address (1-100)."""
        if not (1 <= level <= 100):
            raise ValueError("Level must be between 1 and 100.")
        self._eos.conn.send_message(OSCMessage(address=f"/eos/addr/{self.address_number}", args=(OSCFloat(value=level),)))

    def set_value(self, value: int) -> None:
        """Set the value of the address (0-255)."""
        if not (0 <= value <= 255):
            raise ValueError("Value must be between 0 and 255.")
        self._eos.conn.send_message(
            OSCMessage(address=f"/eos/addr/{self.address_number}/dmx", args=(OSCFloat(value=value),))
        )



class eosProgrammer(programmerControl):
    """A class representing the Eos programmer."""

    def __init__(self, eos: "Eos"):
        self._eos = eos

    def channel(self, channel_number: int) -> _eosChannel:
        """Get a channel object for the specified channel number."""
        return _eosChannel(self._eos, channel_number)

    def address(self, address_number: int) -> _eosAddress:
        """Get an address object for the specified absolute address number."""
        return _eosAddress(self._eos, address_number)

    def live(self) -> None:
        """Toggle the live mode of the programmer."""
        self._eos.keys.send_key("live", button_edge=False)

    def blind(self) -> None:
        """Toggle the blind mode of the programmer."""
        self._eos.keys.send_key("blind", button_edge=False)
