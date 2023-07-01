from rest_framework.permissions import IsAuthenticated

from base_django_rest_framework.models import OAuth2Client
from base_django_rest_framework.permissions import ModelPermissions
from base_django_rest_framework.serializers import OAuth2ClientSerializer
from ..model import ModelViewSet


class OAuth2ClientViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ModelPermissions]
    queryset = OAuth2Client.objects.all()
    serializer_class = OAuth2ClientSerializer
    lookup_field = "id"
    lookup_url_kwarg = "oAuth2Client"
    lookup_url_converter = "uuid"
