from dataclasses import dataclass
from typing import Any, TypeVar


@dataclass(kw_only=True)
class Entity:
    id: int | None = None

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)


EntityType = TypeVar("EntityType", bound=Entity)
