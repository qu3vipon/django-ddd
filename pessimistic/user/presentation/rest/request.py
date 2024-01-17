from ninja import Schema


class PostUserCredentialsRequestBody(Schema):
    email: str
    password: str
