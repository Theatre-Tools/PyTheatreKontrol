from typing import Callable

from .eventDefenitions import Event


class eosEvents:
    """A class to interact with native PyOSC event handling mechanisms to abstractify the creation of event handlers for predefined Eos events."""

    def __init__(self, eos):
        self.eos = eos

    def register_event_handler(self, event_type: Event, handler: Callable[[Event], None]) -> None:
        """Registers an event handler for the given event type."""
        self.eos.conn.register_handler(message_address=event_type.address, validator=event_type.validator, func=handler)

    def handler(self) -> Callable[[Event], None]:
        """Returns a callable that can be used to register an event handler for the given event type."""

        def _handler() -> None:
            """A callable that can be used to register an event handler for the given event type."""
            self.eos.conn.register_handler(
                message_address=event_type.address, validator=event_type.validator, func=self.eos.event_handler
            )

        return _handler
