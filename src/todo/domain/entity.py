from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from shared.domain.entity import Entity
from user.domain.entity import User


@dataclass(eq=False)
class ToDo(Entity):
    contents: str
    due_datetime: datetime | None
    user: User

    @classmethod
    def new(cls, contents: str, due_datetime: datetime | None, user: User) -> ToDo:
        return cls(contents=contents, due_datetime=due_datetime, user=user)

    def update_contents(self, contents: str) -> None:
        self.contents = contents

    def update_due_datetime(self, due_datetime: datetime) -> None:
        self.due_datetime = due_datetime
