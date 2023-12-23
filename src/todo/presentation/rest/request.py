from pydantic import BaseModel


class PostTodoRequestBody(BaseModel):
    todo: str
