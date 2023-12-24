import inspect
import json
from enum import Enum
from typing import Callable, Dict, ItemsView, TypeVar

from django.http import HttpRequest, JsonResponse
from pydantic import BaseModel, ValidationError

from shared.domain.exception import NotAuthorizedException
from shared.infra.authentication import AuthHeader


def health_check(request: HttpRequest):
    return JsonResponse({"status": "ok"})


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    DELETE = "DELETE"


RequestBodyModel = TypeVar("RequestBodyModel", bound=BaseModel)


def handle_request(request: HttpRequest, request_handler: Callable, **kwargs) -> JsonResponse:
    # inspect request_handler signature
    signature: inspect.Signature = inspect.signature(request_handler)
    request_handler_params: ItemsView = signature.parameters.items()

    if request_handler_params:
        for param_name, param_type in request_handler_params:
            type_annotation: type = param_type.annotation

            # user header
            if issubclass(type_annotation, AuthHeader):
                bearer_header: str | None = request.headers.get("Authorization")
                if not bearer_header:
                    return JsonResponse(NotAuthorizedException.message, status=401, safe=False)

                token: str = bearer_header.split(" ")[1]
                try:
                    kwargs["auth_header"] = type_annotation(token=token)
                except ValidationError as e:
                    return JsonResponse(str(e), status=400, safe=False)

            # request body
            elif issubclass(type_annotation, BaseModel):
                try:
                    raw_data: str = request.body.decode("UTF-8")
                    kwargs["body"] = type_annotation(**json.loads(raw_data))
                except ValidationError as e:
                    return JsonResponse(str(e), status=400, safe=False)

        return request_handler(**kwargs)
    return request_handler()


def route(method_handler_map: Dict[str, Callable]) -> Callable:
    def decorator(request: HttpRequest, **kwargs):
        request_handler: Callable | None = method_handler_map.get(request.method)
        if request_handler is None:
            return JsonResponse("Method Not Allowed", status=405, safe=False)
        return handle_request(request=request, request_handler=request_handler, **kwargs)

    return decorator
