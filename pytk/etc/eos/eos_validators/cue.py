from pyosc import OSCFloat
from pydantic import BaseModel

class ActiveCueValidator(BaseModel):
    address: str
    args: tuple[OSCFloat]
    
    @property
    def number(self) -> float:
        splits = self.address.split("/")
        return float(splits[6])
    
    @property
    def list(self) -> float:
        splits = self.address.split("/")
        return float(splits[5])
    
    @property
    def completion(self) -> float:
        return self.args[0].value * 100

class ActiveCompletionValidator(BaseModel):
    args: tuple[OSCFloat]
        
    @property
    def completion(self) -> float:
        return self.args[0].value * 100
    
class PendingCueValidator(BaseModel):
    address: str
    
    @property
    def number(self) -> float:
        splits = self.address.split("/")
        return float(splits[6])
    
    @property
    def list(self) -> float:
        splits = self.address.split("/")
        return float(splits[5])
    
    @property
    def part(self) -> float:
        splits = self.address.split("/")
        if len(splits) < 8:
            return 1
        else:
            return float(splits[7])