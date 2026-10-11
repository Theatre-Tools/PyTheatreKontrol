from pydantic import BaseModel

from .source import sourceTypes


class supportedFeatures(BaseModel):
    """A model representing the supported features of a projector."""

    zoom: bool = False
    focus: bool = False
    shutter: bool = False
    interchangeable_lens: bool = False
    sources: int = 1
    source_type: sourceTypes | None = None
    resolution: str | None = None
    source_wattage: int | None = None
    inputs: list[str] | None = None
    outputs: list[str] | None = None
    control_protocols: list[str] | None = None
