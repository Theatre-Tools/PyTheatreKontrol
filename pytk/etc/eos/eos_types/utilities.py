from dataclasses import dataclass


@dataclass
class PingResponse:
    message: str
    latency: float
    


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
    
