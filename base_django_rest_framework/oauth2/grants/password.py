from authlib.oauth2.rfc6749.grants import ResourceOwnerPasswordCredentialsGrant
from django.contrib.auth import get_user_model

from base_django_rest_framework.models import OAuth2Token
from base_django_rest_framework.serializers import OAuth2TokenSerializer


class PasswordGrant(ResourceOwnerPasswordCredentialsGrant):
    TOKEN_ENDPOINT_AUTH_METHODS = ["none"]

    def authenticate_user(self, username, password):
        try:
            user = get_user_model().objects.get_by_natural_key(username)
            if user.check_password(password):
                return user
        except get_user_model().DoesNotExist:
            return None

    def create_token_response(self):
        status_code, body, headers = super().create_token_response()
        return status_code, OAuth2TokenSerializer(OAuth2Token.objects.get(**body)).data, headers
