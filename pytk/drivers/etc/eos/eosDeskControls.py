from pyosc import OSCFloat, OSCInt, OSCMessage


class eosDeskControls:
    class _macro:
        def __init__(self, eos):
            self._eos = eos

        def __call__(self, macro: float | int):
            """Fire a specific macro on the Eos device."""
            return _macro(self._eos, macro)

    def __init__(self, eos):
        self._eos = eos
        self.macro = self._macro(eos)


class _macro:
    def __init__(self, _eos, macro: float | int):
        self._eos = _eos
        self.macro = macro

    def fire(self):
        """Fire a specific macro on the Eos device."""
        if isinstance(self.macro, (float)):
            arg = OSCFloat(value=self.macro)

        else:
            arg = OSCInt(value=self.macro)

        self._eos.conn.send_message(OSCMessage(address="/eos/macro/fire", args=(arg,)))

    def select(self):
        """Select a specific macro on the Eos device."""
        if isinstance(self.macro, (float)):
            arg = OSCFloat(value=self.macro)
        else:
            arg = OSCInt(value=self.macro)

        self._eos.conn.send_message(OSCMessage(address="/eos/macro", args=(arg,)))
