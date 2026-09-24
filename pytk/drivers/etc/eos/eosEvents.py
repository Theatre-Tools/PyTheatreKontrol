from typing import Callable

from .eventDefenitions import Event


class eosEvents:
    """A class to interact with native PyOSC event handling mechanisms to abstractify the creation of event handlers for predefined Eos events."""

    def __init__(self, eos):
        self.eos = eos

    def register_event_handler(self, event_type, handler: Callable) -> None:
        """Registers an event handler for the given event type."""
        self.eos.conn.register_handler(message_address=event_type.address, validator=event_type.validator, func=handler)

    def handler(self, event: Event) -> Callable[[Callable[[Event], None]], Callable[[Event], None]]:
        """Returns a callable that can be used to register an event handler for the given event type."""

        def handler_decorator(func: Callable[[Event], None]) -> Callable[[Event], None]:
            """A callable that can be used to register an event handler for the given event type."""
            self.eos.conn.register_handler(message_address=event.address, validator=event.validator, func=func)

            return func
        return handler_decorator
