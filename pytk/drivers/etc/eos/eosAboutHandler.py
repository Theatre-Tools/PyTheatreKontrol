from .eosEventValidators import eosLockEventValidator
from .eosAboutValidators import eosVersionValidator

from Typing import TYPE_CHECKING

from pyosc import OSCMessage

if TYPE_CHECKING:
    from .eos import Eos

class eosAboutHandler:
    def __init__(self, eos: Eos):
        self.eos = eos

    def eos_about_handler(self, message: eosVersionValidator | eosLockEventValidator | OSCMessage) -> None:
        """Handles all utility based eos info endpoints by default for the eos.about property"""
        if isinstance(message, eosVersionValidator):
            self.eos.about.software_version = message.software_version
            self.eos.about.fixture_library_version = message.fixture_library_version
            self.eos.about.gel_swatch_type = message.gel_swatch_type
        elif isinstance(message, eosLockEventValidator):
            self.eos.about.locked = message.locked
        else:
            raise ValueError(f"Unexpected message type: {type(message)}")

def register_about_handlers(eos: Eos):
    """Registers the about handlers for the eos device"""
    eos.conn.register_handler(message_address="/eos/out/get/version", func=eos._about_handler.eos_about_handler, validator=eosVersionValidator)
    eos.conn.register_handler(message_address="/eos/out/lock", func=eos._about_handler.eos_about_handler, validator=eosLockEventValidator)