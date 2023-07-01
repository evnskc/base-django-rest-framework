from django.urls import (path, include)

app_name = "base_django_rest_framework"

urlpatterns = [
    path("oauth2/", include("base_django_rest_framework.urls.oauth2")),
    path("users/", include("base_django_rest_framework.urls.user"))
]
