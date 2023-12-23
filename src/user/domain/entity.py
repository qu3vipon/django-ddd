from __future__ import annotations

from dataclasses import dataclass

from shared.domain.entity import Entity


@dataclass(eq=False)
class User(Entity):
    email: str
    password: str

    @classmethod
    def new(cls, email: str, password: str) -> User:
        return cls(email=email, password=password)
