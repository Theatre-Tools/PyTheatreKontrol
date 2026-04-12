from pyosc import OSCString
from datetime import datetime
from ..eos_types.version import FileTypeVersion
from pydantic import BaseModel


class FilePathValidator(BaseModel):
    args: tuple[OSCString]

    @property
    def fullpath(self) -> str:
        return self.args[0].value

    @property
    def filename(self) -> str:
        return self.fullpath.split("/")[-1][:-26]

    @property
    def disk(self) -> str:
        """May not work as intended on non windows based systems (e.g. MacOS ETC Nomad, Wine)

        Returns:
            str: The disk letter of the current show file.
        """
        return self.fullpath.split(":")[0]

    @property
    def latest_quicksave(self) -> datetime:
        ## The last 26 characters contain the quicksave time and date. We remove the leading space and work with that.
        return datetime.strptime(self.fullpath[-25:-6], "%Y-%m-%d %H-%M-%S")

    @property
    def extension(self) -> FileTypeVersion:
        if self.fullpath.endswith(".esf"):
            return FileTypeVersion.ESF
        elif self.fullpath.endswith(".esf2"):
            return FileTypeVersion.ESF2
        elif self.fullpath.endswith(".esf3d"):
            return FileTypeVersion.ESF3D
        else:
            raise ValueError(f"Unknown file extension for show file: {self.fullpath}")
