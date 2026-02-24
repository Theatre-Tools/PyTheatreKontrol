from typing import Optional

from pyosc import CallHandler, OSCFraming, OSCMessage, OSCModes, OSCString, Peer

from .eos_types import PingResponse
from .eos_validators import PingValidator


class EOS:
    def __init__(
        self,
        host: str,
        port: int = 3032,
        mode: OSCModes = OSCModes.TCP,
        framing: OSCFraming = OSCFraming.OSC11,
        bind_ip: Optional[str] = None,
        bind_port: Optional[int] = None,
    ):
        self.host = host
        self.port = port
        self.mode = mode
        self.framing = framing

        if mode == OSCModes.TCP:
            instance = Peer(host, port, mode=OSCModes.TCP, framing=framing)
        elif mode == OSCModes.UDP:
            instance = Peer(host, port, mode=OSCModes.UDP, framing=framing, bind_ip=bind_ip, bind_port=bind_port)  # type: ignore
        else:
            raise ValueError("Invalid mode. Must be either OSCModes.TCP or OSCModes.UDP.")
        self.instance = instance
        self.caller = CallHandler(instance)
        self.instance.start_listening()

    def ping(self, ping_message: str) -> PingResponse | None:
        message = OSCMessage(address="/eos/ping", args=(OSCString(value=ping_message),))
        response = self.caller.call(message=message, return_address="/eos/out/ping", validator=PingValidator)
        try:
            if response and type(response.message) is str:
                if response.message != ping_message:
                    raise ValueError(f"Unexpected ping response message: {response.message}. Expected: {ping_message}")
                return PingResponse(message=response.message)

        except Exception as e:
            raise RuntimeError(f"Error processing ping response: {e}")
