from abc import ABC, abstractmethod


class Device(ABC):
    """A base class for all devices and device classes."""
    def __init__(self, device_id: str, name: str):
        self.device_id = device_id
        self.name = name

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        ...
