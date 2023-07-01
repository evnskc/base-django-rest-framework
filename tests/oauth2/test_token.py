from io import StringIO

from django.core.management import call_command
from django.urls import reverse

from base_django_rest_framework.models import OAuth2Token
from .. import TestCase


class OAuth2TokenTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.list_url = reverse("base_django_rest_framework:oAuth2:tokens:oAuth2Token-list")
        cls.revoke_url = reverse("base_django_rest_framework:oAuth2:tokens:oAuth2Token-revoke")

    def test_urls(self):
        self.assertURLEqual(self.list_url, "/oauth2/tokens/")
        self.assertURLEqual(self.revoke_url, "/oauth2/tokens/revoke/")

    def test_list(self):
        data = self._test_list(check_verification=False, check_permissions=False)
        tokens = data["results"]
        self.assertEqual(data["count"], 3)
        for token in tokens:
            self.check_token(token)

    def test_create(self):
        self._test_create({
            "client_id": self.oauth2_client.client_id,
            "grant_type": "password",
            "username": self.user.get_username(),
            "password": "password"
        })

        self._test_create({
            "client_id": self.oauth2_client.client_id,
            "grant_type": "refresh_token",
            "refresh_token": self.oauth2_token.refresh_token,
        })
        self.assertFalse(OAuth2Token.objects.filter(id=self.oauth2_token.id).exists())

    def test_revoke_using_access_token(self):
        self._test_revoke(self.oauth2_token.access_token)
        self.assertFalse(OAuth2Token.objects.filter(id=self.oauth2_token.id).exists())

    def test_revoke_using_refresh_token(self):
        self._test_revoke(self.oauth2_token.refresh_token)
        self.assertFalse(OAuth2Token.objects.filter(id=self.oauth2_token.id).exists())

    def test_delete_revoked_tokens(self):
        out = StringIO()
        call_command("delete_revoked_oauth2_tokens", stdout=out)
        self.assertIn("Successfully deleted 1 tokens.", out.getvalue())

    def test_delete_expired_tokens(self):
        out = StringIO()
        call_command("delete_expired_oauth2_tokens", stdout=out)
        self.assertIn("Successfully deleted 1 tokens.", out.getvalue())

    def _test_create(self, data, **kwargs):
        self.setUpAuthentication()
        self.assertForbidden(self.client.post(self.list_url, secure=True))

        self.client.logout()

        response = self.client.post(self.list_url, data, format="multipart", secure=True)

        self.assertOk(response)

        token, client = self.check_token(response.json())

        self.assertEqual(client["client_id"], self.oauth2_client.client_id)
        self.assertEqual(client["client_name"], self.oauth2_client.client_name)

        self.assertTrue(OAuth2Token.objects.filter(
            **token, **{"client": self.oauth2_client.client_id, "user": self.user}
        ).exists())

    def _test_revoke(self, token):
        self.assertUnAuthorized(self.client.post(self.revoke_url))
        self.setUpAuthentication()

        response = self.client.post(self.revoke_url, {
            "client_id": self.oauth2_client.client_id,
            "token": token
        }, format="multipart", secure=True)
        self.assertOk(response)
        self.assertJSONEqual(response.content, {})

    def check_token(self, token):
        self.assertIsInstance(token, dict)
        self.assertEqual(list(token.keys()), [
            "id",
            "token_type",
            "access_token",
            "refresh_token",
            "scope",
            "revoked",
            "issued_at",
            "expires_in",
            "client"
        ])

        client = token.pop("client")
        self.assertIsInstance(client, dict)
        self.assertEqual(list(client.keys()), [
            "client_id",
            "client_name"
        ])

        return token, client
