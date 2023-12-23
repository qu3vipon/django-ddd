from datetime import datetime

from pydantic import BaseModel


class PostTodoRequestBody(BaseModel):
    contents: str
    due_datetime: datetime | None = None
