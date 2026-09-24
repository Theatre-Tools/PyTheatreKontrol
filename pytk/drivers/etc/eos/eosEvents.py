from typing import Callable, TypeVar

from pydantic import BaseModel

from .eventDefenitions import Event

T = TypeVar("T", bound=BaseModel)


class eosEvents:
    """A class to interact with native PyOSC event handling mechanisms to abstractify the creation of event handlers for predefined Eos events."""

    def __init__(self, eos):
        self.eos = eos

    def register_event_handler(self, event_type, handler: Callable) -> None:
        """Registers an event handler for the given event type."""
        self.eos.conn.register_handler(message_address=event_type.address, validator=event_type.validator, func=handler)

    def handler(self, event: Event[T]) -> Callable[[Callable[[T], None]], Callable[[T], None]]:
        """Returns a callable that can be used to register an event handler for the given event type."""

        def handler_decorator(func: Callable[[T], None]) -> Callable[[T], None]:
            """A callable that can be used to register an event handler for the given event type."""
            self.eos.conn.register_handler(message_address=event.address, validator=event.validator, func=func)

            return func

        return handler_decorator
