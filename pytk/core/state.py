from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum


class State(Enum):
    """The Connection state of a device."""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    ERROR = "error"

@dataclass(slots=True)
class DeviceState:
    """
    A common state that every PyTK compatible device should be expcted to have. This state is used to track the connection state of a device and the last time it was reached.
    """
    connection: State = State.DISCONNECTED
    online: bool = False
    last_seen: datetime | None = None
    last_error: Exception | None = None

    def seen(self):
        """Bring the device up and update the last seen time to now."""
        self.online = True
        self.last_seen = datetime.now(UTC)
