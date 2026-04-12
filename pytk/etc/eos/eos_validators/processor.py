from pydantic import BaseModel
from pyosc import OSCInt, OSCString, OSCTrue, OSCFalse


class numProcessors(BaseModel):
    address: str
    args: tuple[OSCInt, ...]

    @property
    def num_processors(self) -> int:
        if self.args[0]:
            try:
                return self.args[0].value
            except (IndexError, AttributeError):
                raise ValueError("Invalid argument for processors message. Expected an integer.")
        raise ValueError("No arguments provided for processors message.")


class Processor_Info(BaseModel):
    args: tuple[OSCInt, OSCInt, OSCTrue | OSCFalse, OSCInt, OSCString, OSCString, OSCString, OSCString, OSCString]

    @property
    def processor_id(self) -> int:
        return self.args[0].value

    @property
    def backup_id(self) -> int:
        return self.args[1].value

    @property
    def host_flag(self) -> bool:
        if isinstance(self.args[2], OSCTrue):
            return True
        elif isinstance(self.args[2], OSCFalse):
            return False
        else:
            raise ValueError("Invalid argument for host flag. Expected OSCTrue or OSCFalse.")

    @property
    def health_status(self) -> int:
        return self.args[3].value

    @property
    def label(self) -> str:
        return self.args[4].value

    @property
    def name(self) -> str:
        return self.args[5].value

    @property
    def description(self) -> str:
        return self.args[6].value

    @property
    def IP_address(self) -> str:
        return self.args[7].value

    @property
    def universe_string(self) -> str:
        return self.args[8].value
