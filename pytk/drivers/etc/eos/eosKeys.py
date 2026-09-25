from typing import TYPE_CHECKING

from pyosc import OSCMessage
from pyosc.types import OSCFloat

from .eosEventValidators import eosSoftKeyEventValidator

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

    def _eos_softkey_handler(self, message: eosSoftKeyEventValidator | OSCMessage) -> None:
        """Handles soft key events from the Eos device."""
        if isinstance(message, eosSoftKeyEventValidator):
            self.eos.softkeys._softkeys[message.key_id] = message.key_text
        else:
            raise ValueError(f"Invalid soft key event message type: {type(message)} {message}")


def register_key_handlers(eos: "Eos") -> None:
    """Registers the key handlers for the Eos device."""
    eos.conn.register_handler("/eos/out/softkey/*", func=eos.keys._eos_softkey_handler, validator=eosSoftKeyEventValidator)
