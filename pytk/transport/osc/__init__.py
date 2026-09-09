from typing import Protocol

from pyosc import ConnectionRole, OSCFraming, OSCTransport, Peer


class OSC(Protocol):
    """A protocol for OSC transport classes."""

    def __init__(self, host: str, port: int):
        """Initialize the transport with the given host and port."""
        ...

    def conn(self) -> "Peer":
        """Return the Peer object for the transport."""
        ...


class OSCUDP(OSC):
    """A class for OSC transport over UDP."""

    def __init__(self, host: str, port: int, bind_port: int, bind_ip: str = "0.0.0.0"):
        self.peer = Peer(
            transport=OSCTransport.UDP,
            remote_address=host,
            remote_port=port,
            bind_ip=bind_ip,
            bind_port=bind_port,
            learning=False,
        )

    def conn(self) -> Peer:
        return self.peer


class OSC11(OSC):
    """A class for OSC 1.1 transport over TCP."""

    def __init__(self, host: str, port: int):
        self.peer = Peer(
            connection_role=ConnectionRole.INITIATING,
            transport=OSCTransport.TCP,
            remote_address=host,
            remote_port=port,
            framing=OSCFraming.OSC11,
        )

    def conn(self) -> Peer:
        return self.peer


class OSC10(OSC):
    """A class for OSC 1.0 transport over TCP."""

    def __init__(self, host: str, port: int):
        self.peer = Peer(
            connection_role=ConnectionRole.INITIATING,
            transport=OSCTransport.TCP,
            remote_address=host,
            remote_port=port,
            framing=OSCFraming.OSC10,
        )
