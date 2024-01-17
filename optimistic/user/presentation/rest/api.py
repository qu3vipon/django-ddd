from ninja import Router
from shared.authentication import auth_bearer
from shared.exception import JWTKeyParsingException
from shared.presentation.rest.containers import auth_service
from shared.presentation.rest.response import ErrorMessageResponse, ObjectResponse, error_response, response
from user.application import use_case
from user.domain.models import User
from user.presentation.rest.request import PostUserCredentialsRequestBody
from user.presentation.rest.response import TokenResponse, UserResponse

router = Router(tags=["users"])


@router.post("", response={201: ObjectResponse[UserResponse]})
def sign_up_user_handler(request, body: PostUserCredentialsRequestBody):
    user: User = use_case.sign_up_user(email=body.email, plain_password=body.password)
    return 201, response(UserResponse.build(user=user))


@router.delete(
    "/me",
    auth=auth_bearer,
    response={
        204: None,
        401: ObjectResponse[ErrorMessageResponse],
        404: ObjectResponse[ErrorMessageResponse],
    },
)
def delete_user_me_handler(request):
    try:
        user_id: int = auth_service.get_user_id_from_token(token=request.auth)
    except JWTKeyParsingException as e:
        return 401, error_response(str(e))

    try:
        use_case.delete_user_by_id(user_id=user_id)
    except User.DoesNotExist as e:
        return 404, error_response(str(e))
    return 204, None


@router.post("/log-in", response={200: ObjectResponse[TokenResponse]})
def log_in_user_handler(request, body: PostUserCredentialsRequestBody):
    try:
        jwt_token: str = use_case.log_in_user(email=body.email, plain_password=body.password)
    except User.DoesNotExist as e:
        return 404, error_response(str(e))
    return 200, response(TokenResponse.build(token=jwt_token))
