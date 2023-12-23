from django.urls import path

from shared.presentation.views import HttpMethod, route

from . import views

urlpatterns = [
    path(
        "",
        route(
            {
                HttpMethod.POST: views.sign_up_user_handler,
            }
        ),
    ),
    path(
        "me",
        route(
            {
                HttpMethod.DELETE: views.delete_user_me_handler,
            }
        ),
    ),
    path(
        "log-in",
        route(
            {
                HttpMethod.POST: views.log_in_user_handler,
            }
        ),
    ),
]
