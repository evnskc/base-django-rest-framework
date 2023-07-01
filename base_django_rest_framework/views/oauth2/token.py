from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated

from base_django_rest_framework.oauth2 import server, RevocationEndpoint
from base_django_rest_framework.serializers import OAuth2TokenSerializer
from base_django_rest_framework.throttles import CreateOAuth2TokenRateThrottle
from ..generic import GenericViewSet


class OAuth2TokenViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    serializer_class = OAuth2TokenSerializer

    def get_queryset(self):
        return self.request.user.tokens.all()

    def create(self, request, *args, **kwargs):
        return server.create_token_response(request)

    @action(methods=["post"], detail=False, url_path="revoke", url_name="revoke")
    def revoke(self, request, *args, **kwargs):
        return server.create_endpoint_response(RevocationEndpoint.ENDPOINT_NAME, request)

    def get_throttles(self):
        throttles = super().get_throttles()
        if self.action == self.create.__name__:
            throttles.extend([throttle() for throttle in [CreateOAuth2TokenRateThrottle]])
        return throttles

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.action == self.create.__name__:
            permissions.extend([permission() for permission in [~IsAuthenticated]])
        if self.action in (self.list.__name__, self.revoke.__name__):
            permissions.extend([permission() for permission in [IsAuthenticated]])
        return permissions
