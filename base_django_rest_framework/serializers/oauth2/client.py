from base_django_rest_framework.models import OAuth2Client
from ..model import ModelSerializer


class OAuth2ClientSerializer(ModelSerializer):
    class Meta:
        model = OAuth2Client
        fields = [
            "id",
            "client_id",
            "client_secret",
            "client_name",
            "redirect_uris",
            "default_redirect_uri",
            "scope",
            "response_type",
            "grant_type",
            "token_endpoint_auth_method",
            "client_id_issued_at",
            "client_secret_expires_at"
        ]
        read_only_fields = [
            "id",
            "client_id",
            "client_secret",
            "client_id_issued_at",
            "client_secret_expires_at"
        ]
