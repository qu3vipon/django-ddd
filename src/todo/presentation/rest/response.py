from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel, ConfigDict

from todo.domain.entity import ToDo


class ToDoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    contents: str
    due_datetime: datetime | None = None

    @classmethod
    def build_response(cls, todo: ToDo) -> Dict[str, Any]:
        return cls.model_validate(todo).model_dump()
