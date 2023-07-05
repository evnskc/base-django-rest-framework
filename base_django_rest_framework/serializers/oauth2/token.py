from rest_framework.serializers import Field

from base_django_rest_framework.models import OAuth2Token
from ..model import ModelSerializer


class ClientField(Field):
    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        return {
            "client_id": value.client_id,
            "client_name": value.client_name
        }


class OAuth2TokenSerializer(ModelSerializer):
    client = ClientField()

    class Meta:
        model = OAuth2Token
        fields = [
            "id",
            "token_type",
            "access_token",
            "refresh_token",
            "scope",
            "revoked",
            "issued_at",
            "expires_in",
            "client"
        ]
        read_only_fields = fields
