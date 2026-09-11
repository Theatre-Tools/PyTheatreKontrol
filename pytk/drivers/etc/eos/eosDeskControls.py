from pydantic import BaseModel
from pyosc import OSCMessage
from pyosc.types import OSCInt, OSCString


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


class eosDeskControls:
    class _macro:
        def __init__(self, eos):
            self._eos = eos

        def __call__(self, macro: int):
            """Fire a specific macro on the Eos device."""
            return _macro(self._eos, macro)

    def __init__(self, eos):
        self._eos = eos
        self.macro = self._macro(eos)


class _macro:
    def __init__(self, _eos, macro: int):
        self._eos = _eos
        self.macro = macro

    def fire(self):
        """Fire a specific macro on the Eos device."""
        if self.macro:
            self._eos.conn.send_message(OSCMessage(address="/eos/macro/fire", args=(OSCInt(value=self.macro),)))

    def select(self):
        """Select a specific macro on the Eos device."""
        if self.macro:
            self._eos.conn.send_message(OSCMessage(address="/eos/macro", args=(OSCInt(value=self.macro),)))
