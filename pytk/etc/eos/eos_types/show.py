from dataclasses import dataclass
from datetime import datetime
from .version import FileTypeVersion


@dataclass
class ShowFile:
    disk: str
    filename: str
    fullpath: str
    latest_quicksave: datetime
    extension: FileTypeVersion
