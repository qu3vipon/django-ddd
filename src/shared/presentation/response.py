from typing import Generic, List, TypeVar

from ninja import Schema

T = TypeVar("T")


def response(results: dict | list) -> dict:
    return {"results": results}


class SingleResponse(Schema, Generic[T]):
    results: T


class ListResponse(Schema, Generic[T]):
    results: List[T]


def error_response(msg: str) -> dict:
    return {"results": {"message": msg}}


class ErrorMessageResponse(Schema):
    message: str
