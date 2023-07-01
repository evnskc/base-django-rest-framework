from django.urls import (path, include)

app_name = "oAuth2"

urlpatterns = [
    path("clients/", include("base_django_rest_framework.urls.oauth2.client")),
    path("tokens/", include("base_django_rest_framework.urls.oauth2.token"))
]
