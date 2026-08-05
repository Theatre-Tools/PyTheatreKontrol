from typing import overload

from pyosc import OSCFraming, OSCTransport, Peer

from .cue import Cues
from .eos_types import ActiveQueueItem, PendingQueueItem
from .utilities import Utilities


class EOS:
    @overload
    def __init__(
        self,
        host: str,
        port: int = 3032,
        mode: OSCTransport = OSCTransport.TCP,
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
        mode: OSCTransport = OSCTransport.UDP,
        framing: OSCFraming = OSCFraming.OSC10,
        bind_ip: str = "0.0.0.0",
        bind_port: int = 8001,
    ) -> None: ...

    def __init__(
        self,
        host: str,
        port: int = 3032,
        mode: OSCTransport = OSCTransport.TCP,
        framing: OSCFraming = OSCFraming.OSC11,
        bind_ip: str = "0.0.0.0",
        bind_port: int = 8001,
        keepalive: bool = False,
        keepalive_interval: int = 120,
    ):
        self.host = host
        self.port = port
        self.mode = mode
        self.framing = framing

        if mode == OSCTransport.TCP:
            try:
                instance = Peer(remote_address=host, remote_port=port, transport=OSCTransport.TCP, framing=framing)
            except Exception as e:
                raise RuntimeError(f"Error initializing TCP peer: {e}")
        elif mode == OSCTransport.UDP:
            instance = Peer(
                remote_address=host,
                remote_port=port,
                transport=OSCTransport.UDP,
                framing=framing,
                bind_ip=bind_ip,
                bind_port=bind_port,
            )
        else:
            raise ValueError("Invalid mode. Must be either OSCTransport.TCP or OSCTransport.UDP.")
        self.instance = instance
        self.utilities = Utilities(self)
        self.cue = Cues(self)
        self.instance.start_listening()

        @self.instance.event
        def on_exception(exception: Exception):
            print(f"OSC Peer Exception: {exception}")

        @property
        def active_cue(self) -> ActiveQueueItem | None:
            ## Proxy Method for the cue.active property
            return self.cue.active

        @property
        def pending_cue(self) -> PendingQueueItem | None:
            ## Proxy Method for the cue.pending property
            return self.cue.pending
