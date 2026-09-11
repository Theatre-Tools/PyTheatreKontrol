from enum import Enum

from pydantic import BaseModel
from pyosc.types import OSCInt, OSCString

from pytk.drivers.etc.eos.eosPlaybackTypes import eventTypes


class eosStates(Enum):
    """Contains eos states"""

    BLIND = "blind"
    LIVE = "live"


class eosPlaybackEventValidator(BaseModel):
    """A class to validate messages from the /eos/out/cue/{list}/{cue}/{action} address"""

    @staticmethod
    def _parse_number(value: str) -> int | float:
        try:
            return int(value)
        except ValueError:
            return float(value)

    args: tuple[OSCString]
    address: str

    @property
    def event_type(self) -> eventTypes:
        """Returns the event type of the playback event."""
        try:
            return eventTypes(self.address.split("/")[7])
        except (IndexError, ValueError) as e:
            raise ValueError(f"Invalid address: {self.address}") from e

    @property
    def cue(self) -> int | float | None:
        """Returns the cue associated with the playback event."""
        try:
            return self._parse_number(self.address.split("/")[6])
        except (IndexError, ValueError) as e:
            raise ValueError(f"Invalid address: {self.address}") from e

    @property
    def cue_list(self) -> int | float | None:
        """Returns the cue list associated with the playback event."""
        try:
            return self._parse_number(self.address.split("/")[5])
        except (IndexError, ValueError) as e:
            raise ValueError(f"Invalid address: {self.address}") from e

    @property
    def label(self) -> str | None:
        """Returns the label associated with the playback event."""
        return self.args[0].value if self.args else None


class eosShowSaveEventValidator(BaseModel):
    """A class to validate messages from the /eos/out/show/{state} address"""

    args: tuple[OSCString]
    address: str

    @property
    def state(self) -> str | None:
        """Returns the state associated with the show save event."""
        try:
            return self.address.split("/")[4]
        except IndexError as e:
            raise ValueError(f"Invalid address: {self.address}") from e

    @property
    def show_file(self) -> str | None:
        """Returns the show file associated with the show save event."""
        return self.args[0].value if self.args else None


class eosCmdOutValidator(BaseModel):
    """A class to validate messages from the /eos/out/user/{user_id}/cmd address"""

    args: tuple[OSCString, OSCInt]
    address: str

    @property
    def user_id(self) -> str | None:
        """Returns the user ID associated with the command output event."""
        try:
            return self.address.split("/")[4]
        except IndexError as e:
            raise ValueError(f"Invalid address: {self.address}") from e

    @property
    def command_output(self) -> str | None:
        """Returns the command output associated with the command output event."""
        return self.args[0].value if self.args else None

    @property
    def command_success(self) -> bool | None:
        """Returns True if the command was successful, False if it failed or unknown.
        Arg Value is 0 for success, 1 for failure
        """
        if self.args[1].value == 0:
            return True
        else:
            return False


class eosSoftKeyEventValidator(BaseModel):
    """A class to validate messages from the /eos/out/softkey/{key_id} address"""

    args: tuple[OSCString]
    address: str

    @property
    def key_id(self) -> str | None:
        """Returns the key ID associated with the softkey event."""
        try:
            return self.address.split("/")[4]
        except IndexError as e:
            raise ValueError(f"Invalid address: {self.address}") from e

    @property
    def key_text(self) -> str | None:
        """Returns the key text associated with the softkey event."""
        return self.args[0].value if self.args else None


class eosActiveChannelEventValidator(BaseModel):
    """A class to validate messages from the /eos/out/active/chan address"""

    args: tuple[OSCInt, OSCString]

    @property
    def channel(self) -> int | None:
        """Returns the channel number associated with the active channel event."""
        return self.args[0].value if self.args else None

    @property
    def channel_info(self) -> str | None:
        """Returns the channel info associated with the active channel event."""
        return self.args[1].value if self.args else None


class eosStateEventValidator(BaseModel):
    """A class to validate messages from the /eos/out/event/state address"""

    args: tuple[OSCInt]

    @property
    def state(self) -> eosStates | None:
        """Returns the state associated with the state event."""
        if self.args[0].value == 0:
            return eosStates.LIVE
        elif self.args[0].value == 1:
            return eosStates.BLIND
        else:
            return None

class eosLockEventValidator(BaseModel):
    """A class to validate messages from the /eos/out/event/locked address"""

    args: tuple[OSCInt]

    @property
    def locked(self) -> bool | None:
        """Returns True if the console is locked, False if it is unlocked, or None if unknown."""
        if self.args[0].value == 0:
            return False
        elif self.args[0].value == 1:
            return True
        else:
            return None
