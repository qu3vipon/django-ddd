import inspect
import json
from collections.abc import ValuesView
from enum import Enum
from typing import Any, Callable, Dict, TypeVar

from django.http import HttpRequest, JsonResponse
from pydantic import BaseModel, ValidationError


def health_check(request: HttpRequest):
    return JsonResponse({"status": "ok"})


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


BodyBaseModel = TypeVar("BodyBaseModel", bound=BaseModel)


def handle_post(request: HttpRequest, request_handler: Callable):
    signature: inspect.Signature = inspect.signature(request_handler)
    param_types: ValuesView = signature.parameters.values()
    if param_types:
        # only takes one request body for now
        annotation: BodyBaseModel = next(iter(param_types)).annotation
        try:
            raw_data: str = request.body.decode("UTF-8")
            body: Dict[str, Any] = json.loads(raw_data)
            return request_handler(body=annotation(**body))
        except ValidationError as e:
            return JsonResponse(str(e), status=400, safe=False)
    return request_handler()


def route(method_handler_map: Dict[str, Callable]) -> Callable:
    def decorator(request: HttpRequest, **kwargs):
        request_handler: Callable | None = method_handler_map.get(request.method)
        if request_handler is None:
            return JsonResponse("Method Not Allowed", status=405, safe=False)

        if request.method == HttpMethod.GET:
            return request_handler(**kwargs)
        elif request.method == HttpMethod.POST:
            return handle_post(request=request, request_handler=request_handler)
        return request_handler(request=request)

    return decorator
