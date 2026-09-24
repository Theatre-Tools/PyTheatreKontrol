from dataclasses import dataclass
from typing import Generic, TypeVar

from pydantic import BaseModel

from .eosEventValidators import eosCmdOutValidator, eosLockEventValidator, eosShowSaveEventValidator

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
    CmdMessage = eosCmdOutValidator
    eosLockedEvent = Event[eosLockEventValidator](
        event_type="EosLockEvent", validator=eosLockEventValidator, address="/eos/out/event/locked"
    )
    LockedMessage = eosLockEventValidator
    eosShowSave = Event[eosShowSaveEventValidator](
        event_type="EosShowSaveEvent", validator=eosShowSaveEventValidator, address="/eos/out/event/show/*"
    )
    ShowSaveMessage = eosShowSaveEventValidator
