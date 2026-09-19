from dataclasses import dataclass
from typing import Generic, TypeVar

from pydantic import BaseModel

from .eosEventValidators import eosCmdOutValidator

T = TypeVar("T", bound=BaseModel)


@dataclass(frozen=True)
class Event(Generic[T]):
    event_type: str
    validator: type[T]
    address: str


class Events:
    eosCmdEvent = Event[eosCmdOutValidator](
        event_type="EosCmdEvent",
        validator=eosCmdOutValidator,
        address="/eos/out/user/*/cmd",
    )
    eosCmdOut = eosCmdOutValidator
