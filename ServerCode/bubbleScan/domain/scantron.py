import uuid
import dataclasses

@dataclasses.dataclass
class Scantron:
    code: uuid.UUID
    first: str
    last: str
    idNumber: int
    
    @classmethod
    def from_dict(cls,d):
           return cls(**d)

def tp_dict(self):
    return dataclasses.asdict(self)