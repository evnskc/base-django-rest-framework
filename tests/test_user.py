from io import BytesIO
from urllib.parse import urlparse

from PIL import Image
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.files.storage import default_storage
from django.urls import reverse

from base_django_rest_framework.views import UserViewSet
from . import TestCase


class UserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user2 = get_user_model().objects.get(username="john.doe")

        cls.create_data = {
            "avatar": getattr(cls, "_get_avatar")("avatar.png"),
            "first_name": "First",
            "last_name": "Last",
            "username": "first.last",
            "email": "first.last@example.com",
            "password": "Password#123"
        }

        cls.update_data = {
            "avatar": getattr(cls, "_get_avatar")("avatar_update.png"),
            "first_name": "First Update",
            "last_name": "Last Update",
            "username": "first.last.update"
        }

        cls.partial_update_data = {
            "avatar": getattr(cls, "_get_avatar")("avatar_partial_update.png"),
            "first_name": "First Partial Update"
        }

        cls.partial_update_data2 = {
            "avatar": getattr(cls, "_get_avatar")("avatar_partial_update2.png")
        }

        cls.update_email_data = {"email": "email.update@example.com"}

        cls.update_active_status_data = {"is_active": False}

        cls.update_admin_status_data = {"is_staff": True}

        cls.update_admin_status_data2 = {"is_superuser": True}

        cls.update_admin_status_data3 = {
            "is_staff": False,
            "is_superuser": False
        }

        cls.update_password_data = {"password": "Password#123.update"}

        cls.reset_password_data = {"email": getattr(cls, "user").email}

        cls.reset_password_data2 = {"password": "Password#123.reset"}

        cls.list_url = reverse("base_django_rest_framework:users:user-list")

        cls.detail_url = reverse(
            "base_django_rest_framework:users:user-detail",
            kwargs={UserViewSet.lookup_url_kwarg: getattr(cls, "user").id}
        )
        cls.detail_url2 = reverse(
            "base_django_rest_framework:users:user-detail",
            kwargs={UserViewSet.lookup_url_kwarg: getattr(cls, "user2").id}
        )

        cls.update_email_link_url = reverse("base_django_rest_framework:users:user-email-update-link")
        cls.update_email_url = reverse("base_django_rest_framework:users:user-email-update",
                                       kwargs={"signature": getattr(cls, "user").get_signature(
                                           email=getattr(cls, "update_email_data")["email"])})

        cls.verify_email_link_url = reverse("base_django_rest_framework:users:user-email-verify-link")
        cls.verify_email_url = reverse("base_django_rest_framework:users:user-email-verify",
                                       kwargs={"signature": getattr(cls, "user").get_signature()})

        cls.update_active_status_url = reverse(
            "base_django_rest_framework:users:user-active-update",
            kwargs={UserViewSet.lookup_url_kwarg: getattr(cls, "user").id}
        )
        cls.update_active_status_url2 = reverse(
            "base_django_rest_framework:users:user-active-update",
            kwargs={UserViewSet.lookup_url_kwarg: getattr(cls, "user2").id}
        )

        cls.update_admin_status_url = reverse(
            "base_django_rest_framework:users:user-admin-update",
            kwargs={UserViewSet.lookup_url_kwarg: getattr(cls, "user").id}
        )
        cls.update_admin_status_url2 = reverse(
            "base_django_rest_framework:users:user-admin-update",
            kwargs={UserViewSet.lookup_url_kwarg: getattr(cls, "user2").id}
        )

        cls.update_password_url = reverse("base_django_rest_framework:users:user-password-update")
        cls.reset_password_link_url = reverse("base_django_rest_framework:users:user-password-reset-link")
        cls.reset_password_url = reverse("base_django_rest_framework:users:user-password-reset",
                                         kwargs={"signature": getattr(cls, "user").get_signature()})

    @classmethod
    def _get_avatar(cls, name):
        image = Image.new("RGB", size=(100, 100), color=(0, 0, 0))
        file = BytesIO()
        file.name = name
        image.save(file)
        file.seek(0)
        return file

    def setUpPermission(self, action, model=get_user_model()):
        super().setUpPermission(action, model)

    def test_list(self):
        response_data = self._test_list()
        clients = response_data["results"]
        self.assertEqual(response_data["count"], 2)
        for client in clients:
            self.check_user(client)

    def test_create(self):
        self._test_create(self.create_data, check_authentication=False, check_verification=False,
                          check_permissions=False, format="multipart")

    def test_retrieve_self(self):
        response_data = self._test_retrieve(check_verification=False, check_permissions=False)
        self.check_user(response_data)

    def test_retrieve(self):
        self.detail_url = self.detail_url2
        response_data = self._test_retrieve()
        self.check_user(response_data)

    def test_update_self(self):
        response_data = self._test_update(self.update_data, check_verification=False, check_permissions=False,
                                          format="multipart")
        self.check_user(response_data)
        self.user.refresh_from_db()
        avatar_name = self.check_avatar(response_data.pop("avatar"))
        self.assertEqual(self.user.avatar.name, avatar_name)
        default_storage.delete(avatar_name)
        self.assertDictEqual({
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "username": self.user.username
        }, {key: value for key, value in self.update_data.items() if key != "avatar"})

    def test_update(self):
        self.detail_url = self.detail_url2
        self.setUpAuthentication()
        self.setUpVerification()
        self.setUpPermission("change")
        self.assertForbidden(self.client.put(self.detail_url, self.update_data, format="multipart"))

    def test_partial_update_self(self):
        response_data = self._test_partial_update(self.partial_update_data, check_verification=False,
                                                  check_permissions=False,
                                                  format="multipart")
        self.check_user(response_data)
        self.user.refresh_from_db()
        avatar_name = self.check_avatar(response_data.pop("avatar"))
        self.assertEqual(self.user.avatar.name, avatar_name)
        self.assertDictEqual({
            "first_name": self.user.first_name,
        }, {key: value for key, value in self.partial_update_data.items() if key != "avatar"})

        response_data2 = self._test_partial_update(self.partial_update_data2, check_authentication=False,
                                                   check_verification=False,
                                                   check_permissions=False,
                                                   format="multipart")
        self.assertFalse(default_storage.exists(avatar_name))
        self.check_user(response_data2)
        self.user.refresh_from_db()
        avatar_name2 = self.check_avatar(response_data2.pop("avatar"))
        self.assertEqual(self.user.avatar.name, avatar_name2)
        default_storage.delete(avatar_name2)

    def test_partial_update(self):
        self.detail_url = self.detail_url2
        self.setUpAuthentication()
        self.setUpVerification()
        self.setUpPermission("change")
        self.assertForbidden(self.client.patch(self.detail_url, self.partial_update_data, format="multipart"))

    def test_destroy_self(self):
        self._test_destroy(check_verification=False, check_permissions=False)
        self.assertFalse(get_user_model().objects.filter(id=self.user.id).exists())

    def test_destroy(self):
        file = self._get_avatar("avatar.png")
        self.user2.avatar.save(file.name, file, True)
        self.assertTrue(default_storage.exists(self.user2.avatar.name))
        self.detail_url = self.detail_url2
        self._test_destroy()
        self.assertFalse(get_user_model().objects.filter(id=self.user2.id).exists())
        self.assertFalse(default_storage.exists(self.user2.avatar.name))

    def test_update_email_link(self):
        self.assertUnAuthorized(self.client.post(self.update_email_link_url))
        self.setUpAuthentication()

        self.assertNoContent(self.client.post(self.update_email_link_url, self.update_email_data))

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [f"{self.user.get_full_name()} <{self.update_email_data['email']}>"])
        self.assertEqual(mail.outbox[0].subject, "Email Confirmation")

    def test_update_email(self):
        self.assertNotEqual(self.user.email, self.update_email_data["email"])
        self.assertEqual(self.user.tokens.count(), 3)
        self.assertNoContent(self.client.get(self.update_email_url))
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, self.update_email_data["email"])
        self.assertEqual(self.user.tokens.count(), 0)

    def test_verify_email_link(self):
        self.assertUnAuthorized(self.client.get(self.verify_email_link_url))
        self.setUpAuthentication()

        self.assertNoContent(self.client.get(self.verify_email_link_url))

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [f"{self.user.get_full_name()} <{self.user.email}>"])
        self.assertEqual(mail.outbox[0].subject, "Email Confirmation")

    def test_verify_email(self):
        self.assertFalse(self.user.is_verified)
        self.assertNoContent(self.client.get(self.verify_email_url))
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified)

    def test_update_active_status(self):
        self.assertUnAuthorized(self.client.patch(self.update_active_status_url))
        self.setUpAuthentication()
        self.assertForbidden(self.client.patch(self.update_active_status_url))
        self.setUpVerification()
        self.assertForbidden(self.client.patch(self.update_active_status_url))
        self.setUpPermission("change")
        self.assertForbidden(self.client.patch(self.update_active_status_url))
        self.assertTrue(self.user2.is_active)
        response = self.client.patch(self.update_active_status_url2, self.update_active_status_data)
        self.assertOk(response)
        self.check_user(response.json())
        self.user2.refresh_from_db()
        self.assertFalse(self.user2.is_active)

    def test_update_admin_status(self):
        pass
        self.assertUnAuthorized(self.client.patch(self.update_admin_status_url))
        self.setUpAuthentication()
        self.assertForbidden(self.client.patch(self.update_admin_status_url))
        self.setUpVerification()
        self.assertForbidden(self.client.patch(self.update_admin_status_url))
        self.user.is_superuser = True
        self.user.save()
        self.assertForbidden(self.client.patch(self.update_admin_status_url))
        self.assertFalse(self.user2.is_staff)
        response = self.client.patch(self.update_admin_status_url2, self.update_admin_status_data)
        self.assertOk(response)
        self.check_user(response.json())
        self.user2.refresh_from_db()
        self.assertTrue(self.user2.is_staff)

        self.assertFalse(self.user2.is_superuser)
        response = self.client.patch(self.update_admin_status_url2, self.update_admin_status_data2)
        self.assertOk(response)
        self.check_user(response.json())
        self.user2.refresh_from_db()
        self.assertTrue(self.user2.is_superuser)

        response = self.client.patch(self.update_admin_status_url2, self.update_admin_status_data3)
        self.assertOk(response)
        self.check_user(response.json())
        self.user2.refresh_from_db()
        self.assertFalse(self.user2.is_staff)
        self.assertFalse(self.user2.is_superuser)

    def test_update_password(self):
        self.assertUnAuthorized(self.client.post(self.update_password_url))
        self.setUpAuthentication()

        self.assertEqual(self.user.tokens.count(), 3)
        self.assertFalse(self.user.check_password(self.update_password_data["password"]))
        self.assertNoContent(self.client.post(self.update_password_url, self.update_password_data))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.update_password_data["password"]))
        self.assertEqual(self.user.tokens.count(), 0)

    def test_reset_password_link(self):
        self.setUpAuthentication()
        self.assertForbidden(self.client.post(self.reset_password_link_url))
        self.client.logout()

        self.assertNoContent(self.client.post(self.reset_password_link_url, self.reset_password_data))

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [f"{self.user.get_full_name()} <{self.reset_password_data['email']}>"])
        self.assertEqual(mail.outbox[0].subject, "Password Reset")

    def test_reset_password(self):
        self.setUpAuthentication()
        self.assertForbidden(self.client.post(self.reset_password_url))
        self.client.logout()

        self.assertEqual(self.user.tokens.count(), 3)
        self.assertFalse(self.user.check_password(self.reset_password_data2["password"]))
        self.assertNoContent(self.client.post(self.reset_password_url, self.reset_password_data2))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.reset_password_data2["password"]))
        self.assertEqual(self.user.tokens.count(), 0)

    def _test_create(self, data, **kwargs):
        self.setUpAuthentication()
        self.assertForbidden(self.client.post(self.list_url, **kwargs))
        self.client.logout()

        response_data = super()._test_create(data, **kwargs)
        self.check_user(response_data)
        avatar_name = self.check_avatar(response_data.pop("avatar"))
        response_data.update({"avatar": avatar_name})
        user_query = get_user_model().objects.filter(**response_data)
        self.assertTrue(user_query.exists())
        default_storage.delete(avatar_name)
        user = user_query.get()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [f"{user.get_full_name()} <{user.email}>"])
        self.assertEqual(mail.outbox[0].subject, "Email Confirmation")

    def check_user(self, user):
        self.assertIsInstance(user, dict)
        self.assertEqual(list(user.keys()), [
            "id",
            "avatar",
            "first_name",
            "last_name",
            "username",
            "email",
            "is_verified",
            "is_active",
            "is_staff",
            "is_superuser",
            "created_at",
            "updated_at"
        ])

    def check_avatar(self, avatar):
        media_path = urlparse(settings.MEDIA_URL).path.strip("/")
        avatar_path = urlparse(avatar).path.strip("/")
        avatar_name = "/".join(avatar_path.split("/")[len(media_path.split("/")):])
        self.assertTrue(default_storage.exists(avatar_name))
        return avatar_name
