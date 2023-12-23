from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from shared.domain.entity import Entity


@dataclass(eq=False)
class ToDo(Entity):
    contents: str
    due_datetime: datetime | None

    @classmethod
    def new(cls, contents: str, due_datetime: datetime | None) -> ToDo:
        return cls(contents=contents, due_datetime=due_datetime)
