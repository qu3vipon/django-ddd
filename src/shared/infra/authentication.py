from typing import ClassVar, Dict, Any

import bcrypt
import jwt
from pydantic import BaseModel

from shared.domain.exception import JWTKeyParsingException
from shared.infra.django import settings
from user.domain.entity import User


class AuthHeader(BaseModel):
    token: str


class AuthenticationService:
    SECRET_KEY: ClassVar[str] = settings.SECRET_KEY
    ALGORITHM: ClassVar[str] = "HS256"
    USER_ID_KEY: ClassVar[str] = "user_id"
    HASH_ENCODING: ClassVar[str] = "UTF-8"

    # hash
    def hash_password(self, plain_password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(plain_password.encode(self.HASH_ENCODING), salt=bcrypt.gensalt())
        return hashed_password.decode(self.HASH_ENCODING)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode(self.HASH_ENCODING),
            hashed_password.encode(self.HASH_ENCODING)
        )

    # JWT
    def create_jwt(self, user: User) -> str:
        payload: Dict[str, Any] = {self.USER_ID_KEY: user.id}
        return self._encode_jwt(payload=payload)

    def _encode_jwt(self, payload: Dict[str, Any]) -> str:
        return jwt.encode(payload=payload, key=self.SECRET_KEY, algorithm=self.ALGORITHM)

    def get_user_id_from_token(self, token: str) -> int:
        payload: Dict[str, int] = self._decode_jwt(token=token)
        user_id: int = payload.get(self.USER_ID_KEY, 0)
        # todo: check expiration
        if not user_id:
            raise JWTKeyParsingException()
        return user_id

    def _decode_jwt(self, token: str) -> Dict[str, Any]:
        return jwt.decode(jwt=token, key=self.SECRET_KEY, algorithms=self.ALGORITHM)
