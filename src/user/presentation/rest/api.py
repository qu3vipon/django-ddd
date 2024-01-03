from dataclasses import asdict

from ninja import Router
from shared.domain.exception import JWTKeyParsingException
from shared.infra.authentication import AuthBearer
from shared.infra.di_containers import auth_service
from shared.presentation.response import ErrorMessageResponse, SingleResponse, error_response, response

from user.domain.entity import User
from user.domain.exception import UserNotFoundException
from user.infra.di_containers import user_command
from user.presentation.rest.request import PostUserCredentialsRequestBody
from user.presentation.rest.response import SingleUserResponse, TokenResponse

router = Router(tags=["users"])


@router.post("", response={201: SingleResponse[SingleUserResponse]})
def sign_up_user_handler(request, body: PostUserCredentialsRequestBody):
    user: User = user_command.sign_up_user(email=body.email, plain_password=body.password)
    return 201, response({"user": asdict(user)})


@router.delete(
    "/me",
    auth=AuthBearer(),
    response={
        204: None,
        401: SingleResponse[ErrorMessageResponse],
        404: SingleResponse[ErrorMessageResponse],
    },
)
def delete_user_me_handler(request):
    try:
        user_id: int = auth_service.get_user_id_from_token(token=request.auth)
    except JWTKeyParsingException as e:
        return 401, error_response(str(e))

    try:
        user_command.delete_user_by_id(user_id=user_id)
    except UserNotFoundException as e:
        return 404, error_response(str(e))
    return 204, None


@router.post("/log-in", response={200: SingleResponse[TokenResponse]})
def log_in_user_handler(request, body: PostUserCredentialsRequestBody):
    jwt_token: str = user_command.log_in_user(email=body.email, plain_password=body.password)
    return response({"token": jwt_token})
