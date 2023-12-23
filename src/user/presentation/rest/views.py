from django.http import HttpRequest, JsonResponse


# POST /users/
def sign_up_user_handler() -> JsonResponse:
    return JsonResponse({}, status=201)


# GET /users/me
def get_user_me_handler() -> JsonResponse:
    return JsonResponse({})


# DELETE /users/me
def delete_user_me_handler() -> JsonResponse:
    return JsonResponse({}, status=204)


# POST /users/log-in
def log_in_user_handler() -> JsonResponse:
    return JsonResponse({})
