from abc import ABC

from pytk.core.device import Device

from .projectorPower import ProjectorPowerControl


class Projector(Device, ABC):
    """A protocol for controlling basic functions of a projector."""

    def __init__(self, name: str, device_id: str, serial_number: str):
        super().__init__(name, device_id)
        self.serial_number = serial_number
        self.power = ProjectorPowerControl(projector=self)
