from typing import ClassVar, Dict, Any

import jwt
from pydantic import BaseModel

from shared.domain.exception import JWTKeyParsingException
from shared.infra.django import settings


class AuthHeader(BaseModel):
    token: str


class AuthenticationService:
    SECRET_KEY: ClassVar[str] = settings.SECRET_KEY
    ALGORITHM: ClassVar[str] = "HS256"
    USER_ID_KEY: ClassVar[str] = "user_id"

    def get_user_id_from_token(self, token: str) -> int:
        payload: Dict[str, int] = self._decode_jwt(token=token)
        user_id: int = payload.get(self.USER_ID_KEY, 0)

        # todo: check expiration

        if not user_id:
            raise JWTKeyParsingException()
        return user_id

    def _encode_jwt(self, payload: Dict[str, Any]) -> str:
        return jwt.encode(payload=payload, key=self.SECRET_KEY, algorithm=self.ALGORITHM)

    def _decode_jwt(self, token: str) -> Dict[str, Any]:
        return jwt.decode(jwt=token, key=self.SECRET_KEY, algorithms=self.ALGORITHM)

