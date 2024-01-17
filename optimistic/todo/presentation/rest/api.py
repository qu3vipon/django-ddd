from typing import List

from ninja import Router
from shared.authentication import AuthBearer
from shared.exception import JWTKeyParsingException
from shared.presentation.rest.containers import auth_service
from shared.presentation.rest.response import ErrorMessageResponse, ObjectResponse, error_response, response
from todo.application import use_case
from todo.domain.exception import ToDoNotFoundException
from todo.domain.models import ToDo
from todo.presentation.rest.request import PatchToDoRequestBody, PostToDoRequestBody
from todo.presentation.rest.response import ListToDoResponse, ToDoResponse
from user.application import use_case as user_use_case
from user.domain.models import User

router = Router(tags=["todos"], auth=AuthBearer())


@router.get(
    "/{todo_id}",
    response={
        200: ObjectResponse[ToDoResponse],
        401: ObjectResponse[ErrorMessageResponse],
        404: ObjectResponse[ErrorMessageResponse],
    },
)
def get_todo_handler(request, todo_id: int):
    try:
        user_id: int = auth_service.get_user_id_from_token(token=request.auth)
    except JWTKeyParsingException as e:
        return 401, error_response(str(e))

    try:
        todo: ToDo = use_case.get_todo_of_user(user_id=user_id, todo_id=todo_id)
    except ToDo.DoesNotExist as e:
        return 404, error_response(str(e))

    return 200, response(ToDoResponse.build(todo=todo))


@router.get(
    "",
    response={
        200: ObjectResponse[ListToDoResponse],
        401: ObjectResponse[ErrorMessageResponse],
    },
)
def get_todo_list_handler(request):
    try:
        user_id: int = auth_service.get_user_id_from_token(token=request.auth)
    except JWTKeyParsingException as e:
        return 401, error_response(str(e))

    todos: List[ToDo] = use_case.get_todos_of_user(user_id=user_id)
    return 200, response(ListToDoResponse.build(todos=todos))


@router.post(
    "",
    response={
        201: ObjectResponse[ToDoResponse],
        401: ObjectResponse[ErrorMessageResponse],
        404: ObjectResponse[ErrorMessageResponse],
    },
)
def post_todos_handler(request, body: PostToDoRequestBody):
    try:
        user_id: int = auth_service.get_user_id_from_token(token=request.auth)
    except JWTKeyParsingException as e:
        return 401, error_response(str(e))

    try:
        user: User = user_use_case.get_user(user_id=user_id)
    except User.DoesNotExist as e:
        return 404, error_response(str(e))

    todo: ToDo = use_case.create_todo(user=user, contents=body.contents, due_datetime=body.due_datetime)
    return 201, response(ToDoResponse.build(todo=todo))


@router.patch(
    "/{todo_id}",
    response={
        200: ObjectResponse[ToDoResponse],
        401: ObjectResponse[ErrorMessageResponse],
        404: ObjectResponse[ErrorMessageResponse],
    },
)
def patch_todos_handler(request, todo_id: int, body: PatchToDoRequestBody):
    try:
        user_id: int = auth_service.get_user_id_from_token(token=request.auth)
    except JWTKeyParsingException as e:
        return 401, error_response(str(e))

    try:
        todo: ToDo = use_case.get_todo_of_user(user_id=user_id, todo_id=todo_id)
    except ToDo.DoesNotExist as e:
        return 404, error_response(str(e))

    todo: ToDo = use_case.update_todo(todo=todo, contents=body.contents, due_datetime=body.due_datetime)
    return 200, response(ToDoResponse.build(todo=todo))


@router.delete(
    "/{todo_id}",
    response={
        204: None,
        401: ObjectResponse[ErrorMessageResponse],
        404: ObjectResponse[ErrorMessageResponse],
    },
)
def delete_todos_handler(request, todo_id: int):
    try:
        user_id: int = auth_service.get_user_id_from_token(token=request.auth)
    except JWTKeyParsingException as e:
        return 404, error_response(str(e))

    try:
        use_case.delete_todo_of_user(user_id=user_id, todo_id=todo_id)
    except ToDoNotFoundException as e:
        return 404, error_response(str(e))

    return 204, None
