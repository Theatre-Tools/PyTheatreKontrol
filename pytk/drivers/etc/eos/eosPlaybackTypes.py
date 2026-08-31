from enum import Enum

from pydantic import BaseModel
from pyosc import OSCFloat, OSCString


class eosPlaybackStates(BaseModel):
    """Class to manage the playback states of the EOS driver."""

    active_cue: int | float | None = None
    """The currently active cue. Can be an integer, float, or None if no cue
    is active."""
    pending_cue: int | float | None = None
    """The cue that is pending to be fired. Can be an integer, float, or
    None if no cue is pending."""
    last_cue: int | float | None = None
    """The last cue that was fired. Can be an integer, float, or None if
    no cue has been fired yet."""
    running: bool = False
    """Indicates whether or not there is a fade between cues in progress"""
    stopped: bool = False
    """Indicates whether or not the fade between cues has been stopped. This is only relevant if `running` is True."""
    completion: float | None = None
    """The current completion of the fade between cues. This is a float between 0.0 and 1.0, where 0.0 is the start of the fade and 1.0 is the end of the fade. This is only relevant if `running` is True."""


class eventTypes(Enum):
    """Contains common Eos playback event types."""

    CUE_FIRE = "fire"
    CUE_STOP = "stop"
    CUE_RESUME = "resume"


class eosPlaybackEventValidator(BaseModel):
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


class eosCuePendingValidator(BaseModel):
    """A class to validate the pending cue event from the Eos device."""

    address: str

    @property
    def cue_list(self) -> int | float | None:
        """Returns the cue list associated with the pending cue event."""
        try:
            return int(self.address.split("/")[5])
        except (IndexError, ValueError) as e:
            raise ValueError(f"Invalid address: {self.address}") from e

    @property
    def cue(self) -> int | float | None:
        """Returns the cue associated with the pending cue event."""
        try:
            return int(self.address.split("/")[6])
        except (IndexError, ValueError) as e:
            raise ValueError(f"Invalid address: {self.address}") from e

    @property
    def part(self) -> int | None:
        """Returns the part associated with the pending cue event."""
        try:
            return int(self.address.split("/")[7])
        except (IndexError, ValueError) as e:
            raise ValueError(f"Invalid address: {self.address}") from e


class cueType(BaseModel):
    """A class to represent a cue type in the Eos device."""

    cue_list: int | float
    """The cue list number."""
    cue: int | float
    """The cue number."""
    part: int | None = None
    """The part number. This is optional and can be None if not applicable."""

    """Here are the optional ones"""


class eosActiveCueCompletionValidator(BaseModel):
    """Takes in a message from /eos/out/active/cue and returns the current completion (decimal) within the cue fade."""

    args: tuple[OSCFloat]

    @property
    def completion(self) -> float:
        """Returns the current time within the active cue."""
        try:
            return self.args[0].value
        except (IndexError, ValueError) as e:
            raise ValueError(f"Invalid args: {self.args}") from e


class eosActiveCueValidator(BaseModel):
    """`/eos/out/active/cue/*/* ` - Returns the current active cue and part number."""

    address: str
    args: tuple[OSCFloat]

    @property
    def cue(self) -> int | float:
        """Returns the current active cue number."""
        try:
            return int(self.address.split("/")[6])
        except (IndexError, ValueError) as e:
            raise ValueError(f"Invalid address: {self.address}") from e

    @property
    def cue_list(self) -> int | float:
        """Returns the current active cue list number."""
        try:
            return int(self.address.split("/")[5])
        except (IndexError, ValueError) as e:
            raise ValueError(f"Invalid address: {self.address}") from e

    @property
    def completion(self) -> float:
        """Returns the current time within the active cue."""
        try:
            return self.args[0].value
        except (IndexError, ValueError) as e:
            raise ValueError(f"Invalid args: {self.args}") from e
