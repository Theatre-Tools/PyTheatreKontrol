from abc import ABC

from pytk.av.projectors.projectorPower import ProjectorPowerControl
from pytk.core.device import Device


class Projector(Device, ABC):
    """A protocol for controlling basic functions of a projector."""

    ## Device provides name and device_id attributes
    def __init__(self, name: str, device_id: str, serial_number: str):
        super().__init__(name, device_id)
        self.serial_number = serial_number
        self.power = ProjectorPowerControl(projector=self)
