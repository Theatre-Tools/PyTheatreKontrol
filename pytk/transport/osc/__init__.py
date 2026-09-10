from typing import Protocol

from pyosc import ConnectionRole, OSCFraming, OSCTransport, Peer


class OSC(Protocol):
    """A protocol for OSC transport classes."""

    def __init__(self, host: str, port: int):
        """Initialize the transport with the given host and port."""
        ...

    def peer(self) -> "Peer":
        """Return the Peer object for the transport."""
        ...


class OSCUDP(OSC):
    """A class for OSC transport over UDP."""

    def __init__(self, host: str, port: int, bind_port: int, bind_ip: str = "0.0.0.0"):
        self.host = host
        self.port = port
        self.bind_port = bind_port
        self.bind_ip = bind_ip

    def peer(self) -> Peer:
        return Peer(
            transport=OSCTransport.UDP,
            remote_address=self.host,
            remote_port=self.port,
            bind_ip=self.bind_ip,
            bind_port=self.bind_port,
            learning=False,
        )


class OSC11(OSC):
    """A class for OSC 1.1 transport over TCP."""

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def peer(self) -> Peer:
        return Peer(
            connection_role=ConnectionRole.INITIATING,
            transport=OSCTransport.TCP,
            remote_address=self.host,
            remote_port=self.port,
            framing=OSCFraming.OSC11,
        )


class OSC10(OSC):
    """A class for OSC 1.0 transport over TCP."""

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def peer(self) -> Peer:
        return Peer(
            connection_role=ConnectionRole.INITIATING,
            transport=OSCTransport.TCP,
            remote_address=self.host,
            remote_port=self.port,
            framing=OSCFraming.OSC10,
        )
