from pydantic import BaseModel

class eosVersion(BaseModel):
    major: int
    minor: int
    patch: int
    build: int

class eosVersionValidator(BaseModel):
    args: tuple[str, str, int]

    @property
    def software_version(self) -> eosVersion:
        """Returns the software version as an eosVersion object."""
        major, minor, patch, build = map(int, self.args[0].split('.'))
        build = int(self.args[1])
        return eosVersion(major=major, minor=minor, patch=patch, build=build)

    @property
    def fixture_library_version(self) -> eosVersion:
        """Returns the fixture library version as an eosVersion object."""
        major, minor, patch, build = map(int, self.args[1].split('.'))
        return eosVersion(major=major, minor=minor, patch=patch, build=build)
    @property
    def gel_swatch_type(self) -> int:
        """Returns the gel swatch type as an integer."""
        return int(self.args[2])