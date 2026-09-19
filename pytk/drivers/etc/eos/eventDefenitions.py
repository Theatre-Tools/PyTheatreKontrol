from dataclasses import dataclass

from .eosEventValidators import eosCmdOutValidator


@dataclass
class Event:
    event_type: str
    validator: ...
    address: str


class Events:
    eosCmdEvent = Event(event_type="EosCmdOutEvent", validator=eosCmdOutValidator, address="/eos/out/user/*/cmd")
