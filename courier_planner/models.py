from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Parcel:
    parcel_id: str
    destination: str
    weight: int
    priority: int
    deadline: str
    value: int

    def deadline_key(self):
        return datetime.strptime(self.deadline, "%Y-%m-%d %H:%M")
