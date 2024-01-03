from dataclasses import asdict
from typing import List

from django.http import JsonResponse, HttpRequest
from ninja import Router

from shared.domain.exception import JWTKeyParsingException
from shared.infra.authentication import AuthHeader, AuthBearer
from shared.infra.di_containers import auth_service
from shared.presentation.response import BaseSingleResponse, ErrorMessageResponse, build_response, build_error_response, \
    BaseListResponse
from user.domain.entity import User
from user.domain.exception import UserNotFoundException
from user.infra.di_containers import user_query

from todo.domain.entity import ToDo
from todo.domain.exception import ToDoNotFoundException
from todo.infra.di_containers import todo_command, todo_query
from todo.presentation.rest.request import PatchToDoRequestBody, PostToDoRequestBody
from todo.presentation.rest.response import SingleToDoResponse, ListToDoResponse

router = Router(tags=["todos"], auth=AuthBearer())


@router.get("/{todo_id}", response={
        200: BaseSingleResponse[SingleToDoResponse],
        401: BaseSingleResponse[ErrorMessageResponse],
        404: BaseSingleResponse[ErrorMessageResponse],
    }
)
def get_todo_handler(request, todo_id: int):
    try:
        user_id: int = auth_service.get_user_id_from_token(token=request.auth)
    except JWTKeyParsingException as e:
        return 401, build_error_response(str(e))

    try:
        todo: ToDo = todo_query.get_todo_of_user(user_id=user_id, todo_id=todo_id)
    except ToDoNotFoundException as e:
        return 404, build_error_response(str(e))

    return 200, build_response({"todo": asdict(todo)})


@router.get("", response={
        200: BaseSingleResponse[ListToDoResponse],
        401: BaseSingleResponse[ErrorMessageResponse],
    }
)
def get_todo_list_handler(request):
    try:
        user_id: int = auth_service.get_user_id_from_token(token=request.auth)
    except JWTKeyParsingException as e:
        return 401, build_error_response(str(e))

    todos: List[ToDo] = todo_query.get_todos_of_user(user_id=user_id)
    return 200, build_response({"todos": [asdict(todo) for todo in todos]})


@router.post("", response={
        201: BaseSingleResponse[SingleToDoResponse],
        401: BaseSingleResponse[ErrorMessageResponse],
        404: BaseSingleResponse[ErrorMessageResponse],
    }
)
def post_todos_handler(request, body: PostToDoRequestBody):
    try:
        user_id: int = auth_service.get_user_id_from_token(token=request.auth)
    except JWTKeyParsingException as e:
        return 401, build_error_response(str(e))

    try:
        user: User = user_query.get_user(user_id=user_id)
    except UserNotFoundException as e:
        return 404, build_error_response(str(e))

    todo: ToDo = todo_command.create_todo(user=user, contents=body.contents, due_datetime=body.due_datetime)
    return 201, build_response({"todo": asdict(todo)})


@router.patch("/{todo_id}", response={
        200: BaseSingleResponse[SingleToDoResponse],
        401: BaseSingleResponse[ErrorMessageResponse],
        404: BaseSingleResponse[ErrorMessageResponse],
    }
)
def patch_todos_handler(request, todo_id: int, body: PatchToDoRequestBody):
    try:
        user_id: int = auth_service.get_user_id_from_token(token=request.auth)
    except JWTKeyParsingException as e:
        return 401, build_error_response(str(e))

    try:
        todo: ToDo = todo_query.get_todo_of_user(user_id=user_id, todo_id=todo_id)
    except ToDoNotFoundException as e:
        return 404, build_error_response(str(e))

    todo: ToDo = todo_command.update_todo(todo=todo, contents=body.contents, due_datetime=body.due_datetime)
    return 200, build_response({"todo": asdict(todo)})


@router.delete("/{todo_id}", response={
        204: None,
        401: BaseSingleResponse[ErrorMessageResponse],
        404: BaseSingleResponse[ErrorMessageResponse],
    }
)
def delete_todos_handler(request, todo_id: int):
    try:
        user_id: int = auth_service.get_user_id_from_token(token=request.auth)
    except JWTKeyParsingException as e:
        return 404, build_error_response(str(e))

    try:
        todo_command.delete_todo_of_user(user_id=user_id, todo_id=todo_id)
    except ToDoNotFoundException as e:
        return 404, build_error_response(str(e))

    return 204, None
