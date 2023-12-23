from django.http import HttpRequest, JsonResponse

from todo.domain.entity import ToDo
from todo.infra.di_containers import todo_repo
from todo.presentation.rest.request import PostTodoRequestBody
from todo.presentation.rest.response import TodoResponse


def get_todos_handler(request: HttpRequest) -> JsonResponse:
    return JsonResponse({})


def post_todos_handler(body: PostTodoRequestBody) -> JsonResponse:
    todo: ToDo = ToDo.new(contents=body.contents, due_datetime=body.due_datetime)
    todo: ToDo = todo_repo.save(entity=todo)
    return JsonResponse(
        status=201,
        data={"todo": TodoResponse.model_validate(todo).model_dump()},
    )


def patch_todos_handler(request: HttpRequest) -> JsonResponse:
    return JsonResponse({})


def delete_todos_handler(request: HttpRequest) -> JsonResponse:
    return JsonResponse({}, status=204)
