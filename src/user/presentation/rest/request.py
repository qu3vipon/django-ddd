from pydantic import BaseModel


class PostUserCredentialsRequestBody(BaseModel):
    email: str
    password: str
