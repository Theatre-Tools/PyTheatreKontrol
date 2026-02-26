from time import perf_counter_ns, sleep
from typing import Optional, overload

from pyosc import CallHandler, OSCFraming, OSCMessage, OSCModes, OSCString, Peer

from .eos_types import PingResponse
from .eos_validators import PingValidator

class EOS:
        
    @overload
    def __init__(
        self,
        host: str,
        port: int = 3032,
        mode: OSCModes = OSCModes.TCP,
        framing: OSCFraming = OSCFraming.OSC11,
        bind_ip: None = None,
        bind_port: None = None,
        keepalive: bool = False,
        keepalive_interval: int = 30
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
        keepalive_interval: int = 120

    ):
        self.host = host
        self.port = port
        self.mode = mode
        self.framing = framing

        if mode == OSCModes.TCP:
            instance = Peer(host, port, mode=OSCModes.TCP, framing=framing)
        elif mode == OSCModes.UDP:
            instance = Peer(host, port, mode=OSCModes.UDP, framing=framing, udp_rx_address=bind_ip, udp_rx_port=bind_port)  # type: ignore
        else:
            raise ValueError("Invalid mode. Must be either OSCModes.TCP or OSCModes.UDP.")
        self.instance = instance
        self.caller = CallHandler(instance)
        self.instance.start_listening()

    def ping(self, ping_message: str) -> PingResponse | None:
        start_ns = perf_counter_ns()
        message = OSCMessage(address="/eos/ping", args=(OSCString(value=ping_message),))
        response = self.caller.call(message=message, return_address="/eos/out/ping", validator=PingValidator)
        try:
            if response is None:
                raise RuntimeError("No response received for ping message.")
            if response and type(response.message) is str:
                if response.message != ping_message or response.message == None:
                    raise ValueError(f"Unexpected ping response message: {response.message}. Expected: {ping_message}")
                latency_ms = (perf_counter_ns() - start_ns) / 1_000_000.0
                return PingResponse(message=response.message, latency=latency_ms)

        except Exception as e:
            raise RuntimeError(f"Error processing ping response: {e}")


    
        
    
