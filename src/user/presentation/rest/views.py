from django.http import JsonResponse
from shared.domain.exception import JWTKeyParsingException
from shared.infra.authentication import AuthHeader
from shared.infra.di_containers import auth_service

from user.domain.exception import UserNotFoundException
from user.infra.database.models import User
from user.infra.di_containers import user_command
from user.presentation.rest.request import PostUserCredentialsRequestBody
from user.presentation.rest.response import UserResponse


# POST /users/
def sign_up_user_handler(body: PostUserCredentialsRequestBody) -> JsonResponse:
    user: User = user_command.sign_up_user(email=body.email, plain_password=body.password)
    return JsonResponse(
        data={"user": UserResponse.build_response(user=user)},
        status=201,
    )


# DELETE /users/me
def delete_user_me_handler(auth_header: AuthHeader) -> JsonResponse:
    try:
        user_id: int = auth_service.get_user_id_from_token(token=auth_header.token)
    except JWTKeyParsingException as e:
        return JsonResponse(status=401, data={"message": str(e)})

    try:
        user_command.delete_user_by_id(user_id=user_id)
    except UserNotFoundException as e:
        return JsonResponse(status=404, data={"message": str(e)})
    return JsonResponse({}, status=204)


# POST /users/log-in
def log_in_user_handler(body: PostUserCredentialsRequestBody) -> JsonResponse:
    jwt_token: str = user_command.log_in_user(email=body.email, plain_password=body.password)
    return JsonResponse({"token": jwt_token})
