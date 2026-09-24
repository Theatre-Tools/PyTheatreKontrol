from typing import TYPE_CHECKING

from oscparser import OSCMessage
from pyosc.types import OSCFloat

if TYPE_CHECKING:
    from .eos import Eos


class eosKeys:
    def __init__(self, eos: Eos):
        self.eos = eos

    def send_key(self, key: str, button_edge: bool = False) -> None:
        """Send a key press to the Eos device."""
        if button_edge:
            arg = OSCFloat(value=1.0)
        else:
            arg = OSCFloat(value=0.0)
        self.eos.conn.send_message(OSCMessage(address=f"/eos/keys/{key}", args=(arg,)))
