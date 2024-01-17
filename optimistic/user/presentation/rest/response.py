from __future__ import annotations

from ninja import Schema
from user.domain.models import User


class UserSchema(Schema):
    id: int
    email: str


class UserResponse(Schema):
    user: UserSchema

    @classmethod
    def build(cls, user: User) -> dict:
        return cls(user=UserSchema(id=user.id, email=user.email)).model_dump()


class TokenResponse(Schema):
    token: str

    @classmethod
    def build(cls, token: str) -> dict:
        return cls(token=token).model_dump()
