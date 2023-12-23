from django.http import HttpRequest, JsonResponse

from todo.domain.entity import ToDo
from todo.domain.exception import ToDoNotFoundException
from todo.infra.di_containers import todo_repo
from todo.presentation.rest.request import PostToDoRequestBody, PatchToDoRequestBody
from todo.presentation.rest.response import ToDoResponse


def get_todo_handler(todo_id: int) -> JsonResponse:
    try:
        todo: ToDo = todo_repo.get_todo_by_id(todo_id=todo_id)
    except ToDoNotFoundException as e:
        return JsonResponse(
            status=404, data={"message": str(e)}
        )
    return JsonResponse(
        status=200,
        data={"todo": ToDoResponse.build_response(todo=todo)},
    )


def get_todo_list_handler() -> JsonResponse:
    return JsonResponse({})


def post_todos_handler(body: PostToDoRequestBody) -> JsonResponse:
    todo: ToDo = ToDo.new(contents=body.contents, due_datetime=body.due_datetime)
    todo: ToDo = todo_repo.save(entity=todo)
    return JsonResponse(
        status=201,
        data={"todo": ToDoResponse.build_response(todo=todo)},
    )


def patch_todos_handler(todo_id: int, body: PatchToDoRequestBody) -> JsonResponse:
    try:
        todo: ToDo = todo_repo.get_todo_by_id(todo_id=todo_id)
    except ToDoNotFoundException as e:
        return JsonResponse(
            status=404, data={"message": str(e)}
        )

    if body.contents:
        todo.update_contents(contents=body.contents)

    if body.due_datetime:
        todo.update_due_datetime(due_datetime=body.due_datetime)

    todo: ToDo = todo_repo.save(entity=todo)
    return JsonResponse(
        status=200,
        data={"todo": ToDoResponse.build_response(todo=todo)},
    )


def delete_todos_handler(todo_id: int) -> JsonResponse:
    try:
        todo_repo.delete_todo_by_id(todo_id=todo_id)
    except ToDoNotFoundException as e:
        return JsonResponse(
            status=404, data={"message": str(e)}
        )

    return JsonResponse({}, status=204)
