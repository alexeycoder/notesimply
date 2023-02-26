from datetime import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class Note:
    id: int
    creation_date: datetime
    last_change_date: datetime
    title: str
    body: str
