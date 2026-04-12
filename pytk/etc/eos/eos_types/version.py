from dataclasses import dataclass
from enum import Enum

@dataclass
class VersionResponse:
    eos: 'VersionInfo'
    fixture_lib: 'VersionInfo'
    gel_swatch_type: int

@dataclass
class VersionInfo:
    major: int
    minor: int
    patch: int
    build: int
    


class FileTypeVersion(Enum):
    ESF = 'ESF'
    """Original Eos Showfile. Still supported, generally used for legacy compatability.
    """
    ESF2 = 'ESF2'
    """Eos Showfile version 2. Introduced in Eos v2.9.0. Adds compression.
    """
    ESF3D = 'ESF3D'
    """Eos Showfile version 3D. Introduced in Eos v3.0.0. Adds support for 3D information."""