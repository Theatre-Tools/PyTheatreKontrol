from oscparser import OSCInt, OSCString
from pydantic import BaseModel, ValidationError


class PingValidator(BaseModel):
    address: str
    args: tuple[OSCString]

    @property
    def message(self) -> str:
        if self.args:
            try:
                return self.args[0].value
            except (IndexError, AttributeError):
                raise ValidationError("Invalid argument for ping message. Expected a string.")
        raise ValidationError("No arguments provided for ping message.")
    
    
class VersionInfo(BaseModel):
    version: str

    @property
    def major(self) -> int:
        return int(self.version.split(".")[0])

    @property
    def minor(self) -> int:
        return int(self.version.split(".")[1])

    @property
    def patch(self) -> int:
        return int(self.version.split(".")[2])

    @property
    def build(self) -> int:
        return int(self.version.split(".")[3])    

class VersionValidator(BaseModel):
    address: str
    args: tuple[OSCString, OSCString, OSCInt]

    @property
    def eos(self) -> VersionInfo:
        if self.args and len(self.args) >= 2:
            try:
                version_str = self.args[0].value
                return VersionInfo(version=version_str)
            except (IndexError, AttributeError):
                raise ValidationError("Invalid argument for version message. Expected a string.")
        raise ValidationError("No arguments provided for version message.")
    
    @property
    def fixture_lib(self) -> VersionInfo:
        if self.args and len(self.args) >= 2:
            try:
                version_str = self.args[1].value
                return VersionInfo(version=version_str)
            except (IndexError, AttributeError):
                raise ValidationError("Invalid argument for version message. Expected a string.")
        raise ValidationError("No arguments provided for version message.")
    
    @property
    def gel_swatch_type(self) -> int:
        if self.args and len(self.args) >= 3:
            try:
                return self.args[2].value
            except (IndexError, AttributeError):
                raise ValidationError("Invalid argument for version message. Expected an integer.")
        raise ValidationError("No arguments provided for version message.")
