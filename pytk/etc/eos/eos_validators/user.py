from pydantic import BaseModel, model_validator
from pyosc import OSCInt, OSCString
from dataclasses import dataclass


@dataclass
class User:
    id: int
    console_type: str
    console_name: str


class UserValidator(BaseModel):
    address: str
    args: tuple[OSCInt | OSCString, ...]

    @property
    def users(self) -> list[User]:
        args = self.args

        valid_payload = len(args) % 4 == 0 and all(
            isinstance(args[index], OSCInt) and args[index].value == 3
            for index in range(0, len(args), 4)
        )

        if not valid_payload:
            raise ValueError(
                "Invalid user list message. Expected repeating groups of: "
                "(3, <user id>, <console type>, <console name>)."
            )

        # Each user is represented by a chunk of 4 arguments: (3, <user id>, <console type>, <console name>)
        chunks = [args[index + 1 : index + 4] for index in range(0, len(args), 4)]

        users: list[User] = []
        for user_id, console_type, console_name in chunks:
            if not isinstance(user_id, OSCInt):
                raise ValueError("Invalid user id type in user list message. Expected OSCInt.")
            if not isinstance(console_type, OSCString):
                raise ValueError("Invalid console type in user list message. Expected OSCString.")
            if not isinstance(console_name, OSCString):
                raise ValueError("Invalid console name in user list message. Expected OSCString.")

            users.append(
                User(
                    id=user_id.value,
                    console_type=console_type.value,
                    console_name=console_name.value,
                )
            )
        return users

