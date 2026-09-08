from pyosc import Exceptions

from pytk.core.exceptions import DriverError


class EosSyntaxError(DriverError):
    """Raised when a command sent to the Eos device has a syntax error."""

    pass


class EosConnectionError(Exceptions.SocketError):
    """Raised when there is a connection error with the Eos device."""

    pass
