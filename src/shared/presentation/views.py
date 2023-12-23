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
    PATCH = "PATCH"
    DELETE = "DELETE"


RequestBodyModel = TypeVar("RequestBodyModel", bound=BaseModel)


def handle_post(request: HttpRequest, request_handler: Callable) -> JsonResponse:
    signature: inspect.Signature = inspect.signature(request_handler)
    request_handler_params: ValuesView = signature.parameters.values()
    if request_handler_params:
        # only takes one request body for now
        request_body_model: RequestBodyModel = next(iter(request_handler_params)).annotation
        try:
            raw_data: str = request.body.decode("UTF-8")
            body: Dict[str, Any] = json.loads(raw_data)
            return request_handler(body=request_body_model(**body))
        except ValidationError as e:
            return JsonResponse(str(e), status=400, safe=False)
    return request_handler()


def handle_patch(request: HttpRequest, request_handler: Callable, **kwargs):
    signature: inspect.Signature = inspect.signature(request_handler)
    request_handler_params: ValuesView = signature.parameters.values()
    if request_handler_params:
        # only takes one request body for now
        request_body_model: RequestBodyModel = list(iter(request_handler_params))[-1].annotation
        try:
            raw_data: str = request.body.decode("UTF-8")
            body: Dict[str, Any] = json.loads(raw_data)
            return request_handler(body=request_body_model(**body), **kwargs)
        except ValidationError as e:
            return JsonResponse(str(e), status=400, safe=False)
    return request_handler()


def route(method_handler_map: Dict[str, Callable]) -> Callable:
    def decorator(request: HttpRequest, **kwargs):
        request_handler: Callable | None = method_handler_map.get(request.method)
        if request_handler is None:
            return JsonResponse("Method Not Allowed", status=405, safe=False)

        if request.method in (HttpMethod.GET, HttpMethod.DELETE):
            return request_handler(**kwargs)
        elif request.method == HttpMethod.POST:
            return handle_post(request=request, request_handler=request_handler)
        elif request.method == HttpMethod.PATCH:
            return handle_patch(request=request, request_handler=request_handler, **kwargs)
        return request_handler(request=request)

    return decorator
