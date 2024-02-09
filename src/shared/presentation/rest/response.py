from typing import Generic, TypeVar

from ninja import Schema

T = TypeVar("T")


def response(results: dict | list) -> dict:
    return {"results": results}


class ObjectResponse(Schema, Generic[T]):
    results: T


def error_response(msg: str) -> dict:
    return {"results": {"message": msg}}


class ErrorMessageResponse(Schema):
    message: str
