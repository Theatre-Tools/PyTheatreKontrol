from typing import Optional, overload

from pyosc import OSCFraming, OSCMessage, OSCModes, OSCString, Peer

from .eos_types import PingResponse, VersionResponse
from .eos_validators import PingValidator
from .utilities import Utilities


class EOS:
    @overload
    def __init__(
        self,
        host: str,
        port: int = 3032,
        mode: OSCModes = OSCModes.TCP,
        framing: OSCFraming = OSCFraming.OSC11,
        *,
        keepalive: bool = False,
        keepalive_interval: int = 30,
    ) -> None: ...

    @overload
    def __init__(
        self,
        host: str,
        port: int = 8000,
        mode: OSCModes = OSCModes.UDP,
        framing: OSCFraming = OSCFraming.OSC10,
        bind_ip: str = "0.0.0.0",
        bind_port: int = 8001,
    ) -> None: ...

    def __init__(
        self,
        host: str,
        port: int = 3032,
        mode: OSCModes = OSCModes.TCP,
        framing: OSCFraming = OSCFraming.OSC11,
        bind_ip: Optional[str] = None,
        bind_port: Optional[int] = None,
        keepalive: bool = False,
        keepalive_interval: int = 120,
    ):
        self.host = host
        self.port = port
        self.mode = mode
        self.framing = framing

        if mode == OSCModes.TCP:
            try:
                instance = Peer(host, port, mode=OSCModes.TCP, framing=framing)
            except Exception as e:
                raise RuntimeError(f"Error initializing TCP peer: {e}")
        elif mode == OSCModes.UDP:
            instance = Peer(host, port, mode=OSCModes.UDP, framing=framing, udp_rx_address=bind_ip, udp_rx_port=bind_port)  # type: ignore
        else:
            raise ValueError("Invalid mode. Must be either OSCModes.TCP or OSCModes.UDP.")
        self.instance = instance
        self.utilities = Utilities(self)
        self.instance.start_listening()

        @self.instance.event
        def on_exception(exception: Exception):
            print(f"OSC Peer Exception: {exception}")
