from ninja import Schema


class UserSchema(Schema):
    id: int
    email: str


class SingleUserResponse(Schema):
    user: UserSchema


class TokenResponse(Schema):
    token: str
