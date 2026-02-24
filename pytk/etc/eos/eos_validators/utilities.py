from oscparser import OSCString
from pydantic import BaseModel, ValidationError


class PingValidator(BaseModel):
    address: str
    args: tuple[OSCString]

    @property
    def message(self) -> str | None:
        if self.args:
            try:
                ## Get the value of the response argument
                return self.args[0].value
            except (IndexError, AttributeError):
                raise ValidationError("Invalid argument for ping message. Expected a string.")
        raise ValidationError("No arguments provided for ping message.")
