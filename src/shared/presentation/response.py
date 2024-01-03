from typing import Generic, List, TypeVar

from ninja import Schema

T = TypeVar("T")


def build_response(results: dict | list) -> dict:
    return {"results": results}


class BaseSingleResponse(Schema, Generic[T]):
    results: T


class BaseListResponse(Schema, Generic[T]):
    results: List[T]


def build_error_response(msg: str) -> dict:
    return {"results": {"message": msg}}


class ErrorMessageResponse(Schema):
    message: str
