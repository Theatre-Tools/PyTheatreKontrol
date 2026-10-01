from enum import Enum
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    pass


class ShutterStates(Enum):
    OPEN = False
    CLOSED = True
    UNKNOWN = None


class BaseLenseDriver(Protocol):
    """Minimum interface for a projector lense driver to support."""

    def get_zoom(self) -> float: ...
    def set_zoom(self, zoom: float) -> None: ...
    def get_focus(self) -> float: ...
    def set_focus(self, focus: float) -> None: ...
    def set_shutter(self, open_shutter: bool) -> None: ...
    def get_shutter_state(self) -> ShutterStates: ...



class LenseShutter:
    def __init__(self, driver: BaseLenseDriver):
        self.driver = driver

    def open(self) -> None:
        self.driver.set_shutter(open_shutter=True)

    def close(self) -> None:
        self.driver.set_shutter(open_shutter=False)

    @property
    def state(self) -> ShutterStates:
        return self.driver.get_shutter_state()

    def __repr__(self) -> str:
        return f"<LenseShutter state={self.state.value}>"

    def __call__(self) -> ShutterStates:
        return self.state


class Lense:
    """An abstraction for interfacing with a projector's lense."""

    def __init__(self, driver: BaseLenseDriver):
        self.driver = driver
        self.shutter = LenseShutter(driver=driver)

    def set_zoom(self, zoom: float) -> None:
        if not 0.0 <= zoom <= 100:
            raise ValueError("Zoom must be between 0.0 and 100.0")
        self.driver.set_zoom(zoom=zoom)

    @property
    def zoom(self) -> float:
        return self.driver.get_zoom()

    def set_focus(self, focus: float) -> None:
        if not 0.0 <= focus <= 100:
            raise ValueError("Focus must be between 0.0 and 100.0")
        self.driver.set_focus(focus=focus)

    @property
    def focus(self) -> float:
        return self.driver.get_focus()
