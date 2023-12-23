from django.urls import path

from shared.presentation.views import HttpMethod, route

from . import views

urlpatterns = [
    path(
        "",
        route(
            {
                HttpMethod.GET: views.get_todos_handler,
                HttpMethod.POST: views.post_todos_handler,
                HttpMethod.PATCH: views.patch_todos_handler,
                HttpMethod.DELETE: views.delete_todos_handler,
            }
        ),
    ),
]
