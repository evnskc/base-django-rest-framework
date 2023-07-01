import time

from authlib.integrations.django_oauth2 import token_revoked
from authlib.oauth2.rfc6749 import TokenMixin
from django.conf import settings
from django.db import models

from base_django_rest_framework.managers import OAuth2TokenManager
from .client import OAuth2Client
from ..mixins import UUIDMixin


class OAuth2Token(UUIDMixin, TokenMixin):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="tokens",
        related_query_name="token",
        on_delete=models.CASCADE,
        editable=False)
    client = models.ForeignKey(
        to=OAuth2Client,
        to_field="client_id",
        related_name="tokens",
        related_query_name="token",
        on_delete=models.CASCADE,
        editable=False)
    token_type = models.CharField(max_length=48, editable=False)
    access_token = models.CharField(max_length=48, unique=True, editable=False)
    refresh_token = models.CharField(max_length=48, unique=True, editable=False)
    scope = models.TextField(default="", editable=False)
    revoked = models.BooleanField(default=False, editable=False)
    issued_at = models.BigIntegerField(default=time.time, editable=False)
    expires_in = models.BigIntegerField(default=0, editable=False)

    objects = OAuth2TokenManager()

    class Meta:
        verbose_name = "oAuth2 token"
        verbose_name_plural = "oAuth2 tokens"
        ordering = ["-issued_at"]

    def check_client(self, client):
        return self.client == client

    def get_scope(self):
        return self.scope

    def get_expires_in(self):
        return self.expires_in

    def is_expired(self):
        return getattr(self, "is_expired_")

    def is_revoked(self):
        return self.revoked

    def revoke(self):
        self.revoked = True
        self.save()
        token_revoked.send(sender=self.__class__, token=self)
