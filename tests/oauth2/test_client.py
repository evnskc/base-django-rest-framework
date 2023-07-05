from io import StringIO

from django.core.management import call_command
from django.urls import reverse

from base_django_rest_framework.models import OAuth2Client
from base_django_rest_framework.views import OAuth2ClientViewSet
from .. import TestCase


class OAuth2ClientTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.create_data = {
            "client_name": "client_name",
            "redirect_uris": "redirect_uris",
            "default_redirect_uri": "default_redirect_uri",
            "scope": "scope",
            "response_type": "response_type",
            "grant_type": "password refresh_token",
            "token_endpoint_auth_method": "none"
        }

        cls.update_data = {
            "client_name": f"{getattr(cls, 'oauth2_client').client_name} Update",
            "redirect_uris": "redirect_uris_update",
            "default_redirect_uri": "default_redirect_uri_update",
            "scope": "scope_update",
            "response_type": "response_type_update",
            "grant_type": "client_credentials",
            "token_endpoint_auth_method": "client_secret_basic"
        }

        cls.partial_update_data = {
            "client_name": f"{getattr(cls, 'oauth2_client').client_name} Update"
        }

        cls.list_url = reverse("base_django_rest_framework:oAuth2:clients:client-list")

        cls.detail_url = reverse(
            "base_django_rest_framework:oAuth2:clients:client-detail",
            kwargs={OAuth2ClientViewSet.lookup_url_kwarg: getattr(cls, "oauth2_client").id}
        )

    def setUpPermission(self, action, model=OAuth2Client):
        super().setUpPermission(action, model)

    def test_urls(self):
        self.assertURLEqual(self.list_url, "/oauth2/clients/")
        self.assertURLEqual(self.detail_url, f"/oauth2/clients/{self.oauth2_client.id}/")

    def test_list(self):
        response_data = self._test_list()
        clients = response_data["results"]
        self.assertEqual(response_data["count"], 1)
        for client in clients:
            self.check_client(client)

    def test_create(self):
        response_data = self._test_create(self.create_data)
        self.check_client(response_data)
        self.assertTrue(OAuth2Client.objects.filter(**response_data).exists())

    def test_retrieve(self):
        response_data = self._test_retrieve()
        self.check_client(response_data)

    def test_update(self):
        response_data = self._test_update(self.update_data)
        self.check_client(response_data)
        self.oauth2_client.refresh_from_db()
        self.assertDictEqual({
            "client_name": self.oauth2_client.client_name,
            "redirect_uris": self.oauth2_client.redirect_uris,
            "default_redirect_uri": self.oauth2_client.default_redirect_uri,
            "scope": self.oauth2_client.scope,
            "response_type": self.oauth2_client.response_type,
            "grant_type": self.oauth2_client.grant_type,
            "token_endpoint_auth_method": self.oauth2_client.token_endpoint_auth_method
        }, self.update_data)

    def test_partial_update(self):
        response_data = self._test_partial_update(self.partial_update_data)
        self.check_client(response_data)
        self.oauth2_client.refresh_from_db()
        self.assertDictEqual({"client_name": self.oauth2_client.client_name}, self.partial_update_data)

    def test_destroy(self):
        self._test_destroy()
        self.assertFalse(OAuth2Client.objects.filter(id=self.oauth2_client.id).exists())

    def test_create_default_client(self):
        self._test_create_default_client()
        self._test_create_default_client(client_name="Client Name")

    def _test_create_default_client(self, **kwargs):
        out = StringIO()
        call_command("create_oauth2_client", stdout=out, **kwargs)
        self.assertIn(f"Successfully created {kwargs.get('client_name', 'Default')} OAuth2 Client.", out.getvalue())
        self.assertIn("Client Id : ", out.getvalue())
        self.assertIn("Client Secret : ", out.getvalue())
        self.assertIn("Grant Type : password refresh_token", out.getvalue())
        self.assertIn("Token Endpoint Auth Method : none", out.getvalue())

    def check_client(self, client):
        self.assertIsInstance(client, dict)
        self.assertEqual(list(client.keys()), [
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
        ])
