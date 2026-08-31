from abc import ABC


class Device(ABC):
    def __init__(self, device_id: str, name: str):
        self.device_id = device_id
        self.name = name

    def connect(self):
        pass

    def disconnect(self):
        pass
