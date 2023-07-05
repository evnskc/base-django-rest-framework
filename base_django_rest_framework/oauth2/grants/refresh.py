from authlib.oauth2.rfc6749.grants import RefreshTokenGrant as _RefreshTokenGrant

from base_django_rest_framework.models import OAuth2Token
from base_django_rest_framework.serializers import OAuth2TokenSerializer


class RefreshTokenGrant(_RefreshTokenGrant):
    TOKEN_ENDPOINT_AUTH_METHODS = ["none"]
    INCLUDE_NEW_REFRESH_TOKEN = True

    def authenticate_refresh_token(self, refresh_token):
        try:
            token = OAuth2Token.objects.get(refresh_token=refresh_token)
            if not token.revoked:
                return token
        except OAuth2Token.DoesNotExist:
            return None

    def authenticate_user(self, credential):
        return credential.user

    def revoke_old_credential(self, credential):
        credential.revoke()

    def create_token_response(self):
        status_code, body, headers = super().create_token_response()
        return status_code, OAuth2TokenSerializer(OAuth2Token.objects.get(**body)).data, headers
