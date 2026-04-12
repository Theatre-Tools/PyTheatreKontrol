from dataclasses import dataclass
from datetime import UTC
from re import U

@dataclass
class Part:
    number: float
    label: str
    UTime: float
    DTime: float
    FTime: float
    CTime: float
    BTime: float
    UDelay: float
    DDelay: float
    FDelay: float
    CDelay: float
    BDelay: float
    Duration: float
    

@dataclass
class Cue:
    number: float
    list: float
    label: str
    note: str
    UTime: float
    DTime: float
    FTime: float
    CTime: float
    BTime: float
    UDelay: float
    DDelay: float
    FDelay: float
    CDelay: float
    BDelay: float
    Duration: float
    Parts: list[Part]
    
@dataclass
class ActiveQueueItem:
    number: float
    list: float
    completion: float
    
@dataclass
class PendingQueueItem:
    number: float
    list: float
    part: float