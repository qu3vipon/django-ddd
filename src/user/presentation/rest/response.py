from typing import Any, Dict

from pydantic import BaseModel, ConfigDict

from user.domain.entity import User


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str

    @classmethod
    def build_response(cls, user: User) -> Dict[str, Any]:
        return cls.model_validate(user).model_dump()
