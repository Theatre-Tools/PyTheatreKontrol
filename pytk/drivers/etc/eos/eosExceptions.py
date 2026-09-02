from pytk.core.exceptions import DriverError


class EosSyntaxError(DriverError):
    """Raised when a command sent to the Eos device has a syntax error."""

    pass
