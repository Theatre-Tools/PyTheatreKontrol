from dataclasses import dataclass


@dataclass
class PingResponse:
    message: str
    latency: float
