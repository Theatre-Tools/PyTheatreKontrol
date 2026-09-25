from typing import TYPE_CHECKING

from pyosc import OSCMessage
from pyosc.types import OSCFloat

if TYPE_CHECKING:
    from .eos import Eos


class eosSK:
    """A class to represent the state of the soft keys on an Eos console."""

    def __init__(self, eos: Eos):
        super().__init__()
        self.eos = eos
        self._softkeys = {}

    def softkey_1(self) -> bool:
        """Returns the state of soft key 1."""
        return self._softkeys.get("1", False)

    def softkey_2(self) -> bool:
        """Returns the state of soft key 2."""
        return self._softkeys.get("2", False)

    def softkey_3(self) -> bool:
        """Returns the state of soft key 3."""
        return self._softkeys.get("3", False)

    def softkey_4(self) -> bool:
        """Returns the state of soft key 4."""
        return self._softkeys.get("4", False)

    def softkey_5(self) -> bool:
        """Returns the state of soft key 5."""
        return self._softkeys.get("5", False)

    def softkey_6(self) -> bool:
        """Returns the state of soft key 6."""
        return self._softkeys.get("6", False)

    def softkey_7(self) -> bool:
        """Returns the state of soft key 7."""
        return self._softkeys.get("7", False)

    def softkey_8(self) -> bool:
        """Returns the state of soft key 8."""
        return self._softkeys.get("8", False)

    def softkey_9(self) -> bool:
        """Returns the state of soft key 9."""
        return self._softkeys.get("9", False)

    def softkey_10(self) -> bool:
        """Returns the state of soft key 10."""
        return self._softkeys.get("10", False)

    def softkey_11(self) -> bool:
        """Returns the state of soft key 11."""
        return self._softkeys.get("11", False)

    def softkey_12(self) -> bool:
        """Returns the state of soft key 12."""
        return self._softkeys.get("12", False)

    def more_sk(self):
        """Triggers the 'More SK' action on the Eos console."""
        self.eos.keys.send_key("More_Softkeys", button_edge=False)

    def press_sk(self, key_number: int, button_edge: bool = False) -> None:
        """Presses a specific soft key on the Eos console."""
        if button_edge:
            arg = OSCFloat(value=1.0)
        else:
            arg = OSCFloat(value=0.0)

        if 1 <= key_number <= 12:
            self.eos.conn.send_message(OSCMessage(address=f"/eos/softkey/{key_number}", args=(arg,)))
        else:
            raise ValueError("Soft key number must be between 1 and 12.")
