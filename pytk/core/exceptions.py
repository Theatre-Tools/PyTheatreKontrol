class PyTKError(Exception):
    """Base class for all PyTK exceptions."""

    pass


class UnsupportedFeatureError(PyTKError):
    """Raised when a feature is not supported by a device."""

    pass


class ConnectionError(PyTKError):
    pass


class DeviceOfflineError(ConnectionError):
    pass


class AuthenticationError(ConnectionError):
    pass


class TimeoutError(ConnectionError):
    pass


class ProtocolError(PyTKError):
    pass


class InvalidResponseError(ProtocolError):
    pass


class ChecksumError(ProtocolError):
    pass


class ConfigurationError(PyTKError):
    pass


class DriverNotFoundError(ConfigurationError):
    pass


class InvalidConfigurationError(ConfigurationError):
    pass


class InvalidStateError(PyTKError):
    pass


class DriverError(PyTKError):
    pass


class BusyError(PyTKError):
    pass
