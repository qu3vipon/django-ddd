from __future__ import annotations

from datetime import datetime
from typing import List

from ninja import Schema


class ToDoSchema(Schema):
    id: int
    contents: str
    due_datetime: datetime | None = None


class SingleToDoResponse(Schema):
    todo: ToDoSchema


class ListToDoResponse(Schema):
    todos: List[ToDoSchema]
