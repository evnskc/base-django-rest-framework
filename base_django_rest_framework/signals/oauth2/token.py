from authlib.integrations.django_oauth2 import AuthorizationServer
from authlib.integrations.django_oauth2 import token_revoked
from django.dispatch import receiver

from base_django_rest_framework.models import OAuth2Token


@receiver(token_revoked, sender=OAuth2Token, dispatch_uid="delete token revoked through refresh")
@receiver(token_revoked, sender=AuthorizationServer, dispatch_uid="delete token revoked through revocation endpoint")
def delete_token(sender, token, **kwargs):
    token.delete()
