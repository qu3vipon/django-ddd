from __future__ import annotations

from datetime import datetime
from typing import List

from ninja import Schema

from todo.domain.entity import ToDo


class ToDoSchema(Schema):
    id: int
    contents: str
    due_datetime: datetime | None = None


class ToDoResponse(Schema):
    todo: ToDoSchema

    @classmethod
    def build(cls, todo: ToDo) -> dict:
        return cls(todo=ToDoSchema(id=todo.id, contents=todo.contents, due_datetime=todo.due_datetime)).model_dump()


class ListToDoResponse(Schema):
    todos: List[ToDoSchema]

    @classmethod
    def build(cls, todos: List[ToDo]) -> dict:
        return cls(
            todos=[ToDoSchema(id=todo.id, contents=todo.contents, due_datetime=todo.due_datetime) for todo in todos]
        ).model_dump()
