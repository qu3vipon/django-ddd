from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TodoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    contents: str
    due_datetime: datetime | None = None
