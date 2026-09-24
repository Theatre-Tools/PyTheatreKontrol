from pydantic import BaseModel
from .eosAboutValidators import eosVersion

from datetime import datetime


class eosAbout(BaseModel):
    software_version: eosVersion | None = None
    fixture_library_version: eosVersion | None = None
    gel_swatch_type: int | None = None
    locked: bool | None = None
    show_file: str | None = None
    last_saved: datetime | None = None

