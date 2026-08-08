from dataclasses import dataclass
from typing import Protocol


@dataclass(slots=True, frozen=True)
class Input:
    """
    A common state to describe IO input states.
    """

    id: str
    name: str


class InputControl(Protocol):
    """A protocol for controlling the input state of a device."""

    async def set_input(self, Input) -> None:
        """Set the input state of the device."""
        ...

    async def get_input(self) -> Input | None:
        """Get the details of an input"""
        ...

    async def get_inputs(self) -> list[Input]:
        """Get the details of all inputs"""
        ...
