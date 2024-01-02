from datetime import datetime

from ninja import Schema


class PostToDoRequestBody(Schema):
    contents: str
    due_datetime: datetime | None = None


class PatchToDoRequestBody(Schema):
    contents: str | None
    due_datetime: datetime | None = None
