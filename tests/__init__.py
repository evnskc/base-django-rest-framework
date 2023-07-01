from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from rest_framework.status import (HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_204_NO_CONTENT,
                                   HTTP_201_CREATED)
from rest_framework.test import APITestCase

from base_django_rest_framework.models import OAuth2Client


class TestCase(APITestCase):
    fixtures = ["user.json", "oauth2/client.json", "oauth2/token.json"]

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.first()
        cls.oauth2_client = OAuth2Client.objects.first()
        cls.oauth2_token = getattr(cls, "user").tokens.filter(revoked=False, is_expired_=False).first()

    def setUpAuthentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"{self.oauth2_token.token_type} {self.oauth2_token.access_token}")

    def setUpVerification(self):
        self.user.verify(True)

    def setUpPermission(self, action, model):
        self.user.user_permissions.add(Permission.objects.get(codename=f"{action}_{model._meta.model_name}"))

    def assertUnAuthorized(self, response):
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def assertForbidden(self, response):
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def assertOk(self, response):
        self.assertEqual(response.status_code, HTTP_200_OK)

    def assertCreated(self, response):
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def assertNoContent(self, response):
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

    def _test_list(self, check_authentication=True, check_verification=True, check_permissions=True,
                   permissions=("view",), **kwargs):
        if check_authentication:
            self.assertUnAuthorized(self.client.get(getattr(self, "list_url"), **kwargs))
            self.setUpAuthentication()
        if check_verification:
            self.assertForbidden(self.client.get(getattr(self, "list_url"), **kwargs))
            self.setUpVerification()
        if check_permissions:
            for permission in permissions:
                self.assertForbidden(self.client.get(getattr(self, "list_url"), **kwargs))
                getattr(self, "setUpPermission")(permission)

        response = self.client.get(getattr(self, "list_url"), **kwargs)
        self.assertOk(response)
        return response.json()

    def _test_create(self, data, check_authentication=True, check_verification=True, check_permissions=True,
                     permissions=("add",), **kwargs):
        if check_authentication:
            self.assertUnAuthorized(self.client.post(getattr(self, "list_url"), data, **kwargs))
            self.setUpAuthentication()
        if check_verification:
            self.assertForbidden(self.client.post(getattr(self, "list_url"), data, **kwargs))
            self.setUpVerification()
        if check_permissions:
            for permission in permissions:
                self.assertForbidden(self.client.post(getattr(self, "list_url"), data, **kwargs))
                getattr(self, "setUpPermission")(permission)

        response = self.client.post(getattr(self, "list_url"), data, **kwargs)
        self.assertCreated(response)
        return response.json()

    def _test_retrieve(self, check_authentication=True, check_verification=True, check_permissions=True,
                       permissions=("view",), **kwargs):
        if check_authentication:
            self.assertUnAuthorized(self.client.get(getattr(self, "detail_url"), **kwargs))
            self.setUpAuthentication()
        if check_verification:
            self.assertForbidden(self.client.get(getattr(self, "detail_url"), **kwargs))
            self.setUpVerification()
        if check_permissions:
            for permission in permissions:
                self.assertForbidden(self.client.get(getattr(self, "detail_url"), **kwargs))
                getattr(self, "setUpPermission")(permission)

        response = self.client.get(getattr(self, "detail_url"), **kwargs)
        self.assertOk(response)
        return response.json()

    def _test_update(self, data, check_authentication=True, check_verification=True, check_permissions=True,
                     permissions=("change",), **kwargs):
        if check_authentication:
            self.assertUnAuthorized(self.client.put(getattr(self, "detail_url"), **kwargs))
            self.setUpAuthentication()
        if check_verification:
            self.assertForbidden(self.client.put(getattr(self, "detail_url"), **kwargs))
            self.setUpVerification()
        if check_permissions:
            for permission in permissions:
                self.assertForbidden(self.client.put(getattr(self, "detail_url"), **kwargs))
                getattr(self, "setUpPermission")(permission)

        response = self.client.put(getattr(self, "detail_url"), data, **kwargs)
        self.assertOk(response)
        return response.json()

    def _test_partial_update(self, data, check_authentication=True, check_verification=True, check_permissions=True,
                             permissions=("change",), **kwargs):
        if check_authentication:
            self.assertUnAuthorized(self.client.patch(getattr(self, "detail_url"), **kwargs))
            self.setUpAuthentication()
        if check_verification:
            self.assertForbidden(self.client.patch(getattr(self, "detail_url"), **kwargs))
            self.setUpVerification()
        if check_permissions:
            for permission in permissions:
                self.assertForbidden(self.client.patch(getattr(self, "detail_url"), **kwargs))
                getattr(self, "setUpPermission")(permission)

        response = self.client.put(getattr(self, "detail_url"), data, **kwargs)
        self.assertOk(response)
        return response.json()

    def _test_destroy(self, check_authentication=True, check_verification=True, check_permissions=True,
                      permissions=("delete",), **kwargs):
        if check_authentication:
            self.assertUnAuthorized(self.client.delete(getattr(self, "detail_url"), **kwargs))
            self.setUpAuthentication()
        if check_verification:
            self.assertForbidden(self.client.delete(getattr(self, "detail_url"), **kwargs))
            self.setUpVerification()
        if check_permissions:
            for permission in permissions:
                self.assertForbidden(self.client.delete(getattr(self, "detail_url"), **kwargs))
                getattr(self, "setUpPermission")(permission)
        self.assertNoContent(self.client.delete(getattr(self, "detail_url"), **kwargs))
