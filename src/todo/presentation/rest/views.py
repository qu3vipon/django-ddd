from django.http import JsonResponse

from shared.domain.exception import JWTKeyParsingException
from shared.infra.di_containers import auth_service
from shared.infra.security import AuthHeader
from todo.domain.entity import ToDo
from todo.domain.exception import ToDoNotFoundException
from todo.infra.di_containers import todo_query, todo_command
from todo.presentation.rest.request import PostToDoRequestBody, PatchToDoRequestBody
from todo.presentation.rest.response import ToDoResponse


def get_todo_handler(todo_id: int) -> JsonResponse:
    try:
        todo: ToDo = todo_query.get_todo_by_id(todo_id=todo_id)
    except ToDoNotFoundException as e:
        return JsonResponse(
            status=404, data={"message": str(e)}
        )
    return JsonResponse(
        status=200,
        data={"todo": ToDoResponse.build_response(todo=todo)},
    )


def get_todo_list_handler(auth_header: AuthHeader) -> JsonResponse:
    try:
        user_id: int = auth_service.get_user_id_from_token(token=auth_header.token)
    except JWTKeyParsingException as e:
        return JsonResponse(status=401, data={"message": str(e)})

    # todo
    # user: User = user_repo.get_user_by_user_id(user_id=user_id)

    return JsonResponse({})


def post_todos_handler(body: PostToDoRequestBody) -> JsonResponse:
    todo: ToDo = todo_command.create_todo(contents=body.contents, due_datetime=body.due_datetime)
    return JsonResponse(
        status=201,
        data={"todo": ToDoResponse.build_response(todo=todo)},
    )


def patch_todos_handler(todo_id: int, body: PatchToDoRequestBody) -> JsonResponse:
    try:
        todo: ToDo = todo_query.get_todo_by_id(todo_id=todo_id)
    except ToDoNotFoundException as e:
        return JsonResponse(
            status=404, data={"message": str(e)}
        )

    todo: ToDo = todo_command.update_todo(todo=todo, contents=body.contents, due_datetime=body.due_datetime)
    return JsonResponse(
        status=200,
        data={"todo": ToDoResponse.build_response(todo=todo)},
    )


def delete_todos_handler(todo_id: int) -> JsonResponse:
    try:
        todo_command.delete_todo_by_id(todo_id=todo_id)
    except ToDoNotFoundException as e:
        return JsonResponse(
            status=404, data={"message": str(e)}
        )

    return JsonResponse({}, status=204)
