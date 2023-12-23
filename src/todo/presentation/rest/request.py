from datetime import datetime

from pydantic import BaseModel


class PostToDoRequestBody(BaseModel):
    contents: str
    due_datetime: datetime | None = None


class PatchToDoRequestBody(BaseModel):
    contents: str | None
    due_datetime: datetime | None = None
