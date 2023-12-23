from django.http import HttpRequest, JsonResponse

from todo.presentation.rest.request import PostTodoRequestBody


def get_todos_handler(request: HttpRequest) -> JsonResponse:
    return JsonResponse({})


def post_todos_handler(body: PostTodoRequestBody) -> JsonResponse:
    return JsonResponse({}, status=201)


def patch_todos_handler(request: HttpRequest) -> JsonResponse:
    return JsonResponse({})


def delete_todos_handler(request: HttpRequest) -> JsonResponse:
    return JsonResponse({}, status=204)
