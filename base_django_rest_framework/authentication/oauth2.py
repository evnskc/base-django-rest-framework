from authlib.integrations.django_oauth2 import ResourceProtector, BearerTokenValidator
from authlib.oauth2 import OAuth2Error
from authlib.oauth2.rfc6749 import MissingAuthorizationError
from rest_framework.authentication import BaseAuthentication as _BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from base_django_rest_framework.models import OAuth2Token


class OAuth2Authentication(_BaseAuthentication, ResourceProtector):
    def __init__(self):
        super().__init__()
        self.register_token_validator(BearerTokenValidator(OAuth2Token))

    def authenticate(self, request):
        try:
            token = self.acquire_token(request)
            if not token.user.is_active:
                raise AuthenticationFailed("User inactive or deleted.")
            return token.user, token
        except MissingAuthorizationError:
            return None
        except OAuth2Error as error:
            raise AuthenticationFailed(detail=error.error, code=error.status_code)

    def authenticate_header(self, request):
        return "Bearer <token>"
