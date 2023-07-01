import secrets
import time

from authlib.oauth2.rfc6749 import ClientMixin, scope_to_list, list_to_scope
from django.db import models

from base_django_rest_framework.managers import OAuth2ClientManager
from base_django_rest_framework.utils import client_id_generator
from ..mixins import UUIDMixin


class OAuth2Client(UUIDMixin, ClientMixin):
    client_id = models.CharField(
        max_length=48,
        unique=True,
        editable=False,
        default=client_id_generator)
    client_secret = models.CharField(
        max_length=48,
        blank=True,
        editable=False)
    client_name = models.CharField(max_length=128, unique=True)
    redirect_uris = models.TextField(blank=True, default="")
    default_redirect_uri = models.TextField(blank=True, default="")
    scope = models.TextField(blank=True, default="")
    response_type = models.TextField(blank=True, default="")
    grant_type = models.TextField(blank=True, default="")
    token_endpoint_auth_method = models.CharField(max_length=48, default="client_secret_basic")
    client_id_issued_at = models.BigIntegerField(default=time.time, editable=False)
    client_secret_expires_at = models.BigIntegerField(default=0, editable=False)

    objects = OAuth2ClientManager()

    class Meta:
        verbose_name = "oAuth2 client"
        verbose_name_plural = "oAuth2 clients"
        ordering = ["-client_id_issued_at"]

    def get_client_id(self):
        return self.client_id

    def get_default_redirect_uri(self):
        return self.default_redirect_uri

    def get_allowed_scope(self, scope):
        if not scope:
            return ""
        allowed = set(scope_to_list(self.scope))
        return list_to_scope([s for s in scope.split() if s in allowed])

    def check_redirect_uri(self, redirect_uri):
        return self.default_redirect_uri == redirect_uri or redirect_uri in self.redirect_uris.split()

    def check_client_secret(self, client_secret):
        return secrets.compare_digest(self.client_secret, client_secret)

    def check_endpoint_auth_method(self, method, endpoint):
        if endpoint == "token":
            return self.token_endpoint_auth_method == method
        return True

    def check_response_type(self, response_type):
        return response_type in self.response_type.split()

    def check_grant_type(self, grant_type):
        return grant_type in self.grant_type.split()
