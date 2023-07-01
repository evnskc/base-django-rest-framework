from authlib.integrations.django_oauth2 import AuthorizationServer

from base_django_rest_framework.models import OAuth2Client, OAuth2Token
from .endpoints import RevocationEndpoint
from .grants import PasswordGrant, RefreshTokenGrant

server = AuthorizationServer(OAuth2Client, OAuth2Token)

server.register_endpoint(RevocationEndpoint)

server.register_grant(PasswordGrant)
server.register_grant(RefreshTokenGrant)
