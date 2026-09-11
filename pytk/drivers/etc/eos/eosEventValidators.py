from pydantic import BaseModel
from pyosc.types import OSCString

from pytk.drivers.etc.eos.eosPlaybackTypes import eventTypes


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
