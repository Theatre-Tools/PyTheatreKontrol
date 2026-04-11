from cProfile import label
from dataclasses import dataclass
from typing import List

@dataclass
class Processor:
    """Represents a processor in the Eos system."""
    
    id: int
    """The Internal ID of the processor
    """
    backup_id: int
    """The Backup ID of the processor
    """
    host_flag: bool
    """Indicates if the processor is a host
    """
    health_status: int
    """The health status of the processor
    """
    label: str
    """The label of the processor. This is a user-defineable attribute of each processor.
    """
    name: str
    """The name of the processor. This is the device name attribute of Eos.
    """
    description: str
    """The description of the processor, normally the decvice type (e.g. "ETCNomad")
    """
    IP_address: str
    """The IP address of the processor
    """
    universe_string: str
    """The universe string of the processor"""
    
@dataclass
class ProcResponse:
    """Represents the response from a request for processor information in the Eos system."""
    count: int
    """A count of all the proccessors assigned to the eos session
    """
    processors: List[Processor] | Processor
    """A list of Processor objects representing all the processors assigned to the eos session, or a single Processor object if only one processor is assigned to the session.
    """