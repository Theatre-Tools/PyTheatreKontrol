from enum import Enum


class sourceTypes(Enum):
    """The types of source a projector can have."""

    LASER = "laser"
    UHP = "UHP"
    METAL_HALIDE = "metal halide"
    HALOGEN = "halogen"
    XENON_ARC = "xenon arc"


class sourceStatus(Enum):
    """The status of a projector's source."""

    STRUCK = "struck"
    WARM_SPARE = "warm spare"
    BLOWN = "blown"
    UNKNOWN = "unknown"


class source:
    """A model representing the details of a projector's source."""

    def __init__(self, projector, source_type: sourceTypes, wattage: int | None = None, source_number: int = 1):
        self.projector = projector
        self.source_type = source_type
        self.wattage = wattage
        self.source_number = source_number
        self.driver = projector._driver

    @property
    def get_hours(self) -> int | None:
        """Get the number of hours the source has been used."""
        if hasattr(self.driver, "get_raw_lamp_hours"):
            return self.driver.get_raw_lamp_hours(source_number=self.source_number)
        return None

    @property
    def get_status(self) -> sourceStatus:
        """Get the status of the source."""
        if hasattr(self.driver, "get_raw_source_status"):
            return self.driver.get_raw_source_status(source_number=self.source_number)
        return sourceStatus.UNKNOWN
