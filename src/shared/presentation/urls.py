from django.contrib import admin
from django.urls import include, path

from .views import health_check

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health-check/", health_check, name="health_check_api"),
    path("todos/", include("todo.presentation.rest.urls"), name="todos_api"),
    path("users/", include("user.presentation.rest.urls"), name="users_api"),
]
