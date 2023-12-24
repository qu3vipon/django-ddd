from typing import List

from django.http import JsonResponse
from shared.domain.exception import JWTKeyParsingException
from shared.infra.authentication import AuthHeader
from shared.infra.di_containers import auth_service
from user.domain.entity import User
from user.domain.exception import UserNotFoundException
from user.infra.di_containers import user_query

from todo.domain.entity import ToDo
from todo.domain.exception import ToDoNotFoundException
from todo.infra.di_containers import todo_command, todo_query
from todo.presentation.rest.request import PatchToDoRequestBody, PostToDoRequestBody
from todo.presentation.rest.response import ToDoResponse


def get_todo_handler(auth_header: AuthHeader, todo_id: int) -> JsonResponse:
    try:
        user_id: int = auth_service.get_user_id_from_token(token=auth_header.token)
    except JWTKeyParsingException as e:
        return JsonResponse(status=401, data={"message": str(e)})

    try:
        todo: ToDo = todo_query.get_todo_of_user(user_id=user_id, todo_id=todo_id)
    except ToDoNotFoundException as e:
        return JsonResponse(status=404, data={"message": str(e)})

    return JsonResponse(
        status=200,
        data={"todo": ToDoResponse.build_response(todo=todo)},
    )


def get_todo_list_handler(auth_header: AuthHeader) -> JsonResponse:
    try:
        user_id: int = auth_service.get_user_id_from_token(token=auth_header.token)
    except JWTKeyParsingException as e:
        return JsonResponse(status=401, data={"message": str(e)})

    todos: List[ToDo] = todo_query.get_todos_of_user(user_id=user_id)
    return JsonResponse({"todos": [ToDoResponse.build_response(todo=todo) for todo in todos]})


def post_todos_handler(auth_header: AuthHeader, body: PostToDoRequestBody) -> JsonResponse:
    try:
        user_id: int = auth_service.get_user_id_from_token(token=auth_header.token)
    except JWTKeyParsingException as e:
        return JsonResponse(status=401, data={"message": str(e)})

    try:
        user: User = user_query.get_user(user_id=user_id)
    except UserNotFoundException as e:
        return JsonResponse(status=404, data={"message": str(e)})

    todo: ToDo = todo_command.create_todo(user=user, contents=body.contents, due_datetime=body.due_datetime)
    return JsonResponse(
        status=201,
        data={"todo": ToDoResponse.build_response(todo=todo)},
    )


def patch_todos_handler(auth_header: AuthHeader, todo_id: int, body: PatchToDoRequestBody) -> JsonResponse:
    try:
        user_id: int = auth_service.get_user_id_from_token(token=auth_header.token)
    except JWTKeyParsingException as e:
        return JsonResponse(status=401, data={"message": str(e)})

    try:
        todo: ToDo = todo_query.get_todo_of_user(user_id=user_id, todo_id=todo_id)
    except ToDoNotFoundException as e:
        return JsonResponse(status=404, data={"message": str(e)})

    todo: ToDo = todo_command.update_todo(todo=todo, contents=body.contents, due_datetime=body.due_datetime)
    return JsonResponse(
        status=200,
        data={"todo": ToDoResponse.build_response(todo=todo)},
    )


def delete_todos_handler(auth_header: AuthHeader, todo_id: int) -> JsonResponse:
    try:
        user_id: int = auth_service.get_user_id_from_token(token=auth_header.token)
    except JWTKeyParsingException as e:
        return JsonResponse(status=401, data={"message": str(e)})

    try:
        todo_command.delete_todo_of_user(user_id=user_id, todo_id=todo_id)
    except ToDoNotFoundException as e:
        return JsonResponse(status=404, data={"message": str(e)})

    return JsonResponse({}, status=204)
