import threading
from abc import ABC, abstractmethod
from select import select
from socket import AF_INET, SOCK_STREAM, socket
from typing import Callable


class Serial(ABC):
    """A protocol for Serial transport classes."""

    @abstractmethod
    def connect(self) -> None:
        """Connect to the serial device."""
        ...

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from the serial device."""
        ...

    @abstractmethod
    def send(self, data: bytes) -> None:
        """Send data to the serial device."""
        ...

    @abstractmethod
    def set_receive_callback(self, receiver: Callable[[bytes], None]) -> None:
        """Set a callback function to be called when data is received."""
        ...


class SerialTCP(Serial):
    """A class for Serial transport over TCP."""

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.connection: socket | None = None
        self.receiver: Callable[[bytes], None] | None = None
        self.background: threading.Thread | None = None
        self.stop_flag = threading.Event()

    def connect(self) -> None:
        """Connect to the serial device over TCP."""
        self.connection = socket(AF_INET, SOCK_STREAM)
        self.connection.connect((self.host, self.port))
        self.stop_flag.clear()
        self.background = threading.Thread(target=self._receive_data, daemon=True)
        self.background.start()

    def disconnect(self) -> None:
        """Disconnect from the serial device over TCP."""
        if self.connection and self.background:
            self.stop_flag.set()
            self.connection.close()
            self.background.join()
            self.connection = None
            self.background = None
        else:
            raise RuntimeError("Not connected to the serial device.")

    def send(self, data: bytes) -> None:
        """Send data to the serial device over TCP."""
        if self.connection:
            self.connection.sendall(data)
        else:
            raise RuntimeError("Not connected to the serial device.")

    def set_receive_callback(self, receiver: Callable[[bytes], None]) -> None:
        """Set a callback function to be called when data is received over TCP."""
        self.receiver = receiver

    def _receive_data(self) -> None:
        """Background thread to receive data from the serial device over TCP."""
        while not self.stop_flag.is_set() and self.connection:
            read, _write, _exec = select([self.connection], [], [], 0.01)
            for sock in read:
                data = sock.recv(1024)
                if data and self.receiver:
                    self.receiver(data)
