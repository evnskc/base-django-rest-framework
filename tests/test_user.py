from io import BytesIO
from urllib.parse import urlparse

from PIL import Image
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.urls import reverse

from base_django_rest_framework.views import UserViewSet
from . import TestCase


class UserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user2 = get_user_model().objects.exclude(id=getattr(cls, "user").id).first()
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
        cls.verify_email_link_url = reverse("base_django_rest_framework:users:user-email-verify-link")
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

    def setUpPermission(self, action, model=get_user_model()):
        super().setUpPermission(action, model)

    def test_list(self):
        data = self._test_list()
        clients = data["results"]
        self.assertEqual(data["count"], 2)
        for client in clients:
            self.check_user(client)

    def test_create(self):
        image = Image.new("RGB", size=(100, 100), color=(0, 0, 0))
        file = BytesIO()
        file.name = "avatar.jpg"
        image.save(file)
        file.seek(0)
        self._test_create({
            "avatar": file,
            "first_name": "First",
            "last_name": "Last",
            "email": "first.last@example.com",
            "username": "first.last",
            "password": "Password#123.@"
        }, check_authentication=False, check_verification=False, check_permissions=False, format="multipart")

    def test_retrieve(self):
        pass

    def test_update(self):
        pass

    def test_partial_update(self):
        pass

    def test_destroy(self):
        pass

    def test_update_email(self):
        pass

    def test_verify_email(self):
        pass

    def test_update_active_status(self):
        pass

    def test_update_admin_status(self):
        pass

    def test_update_password(self):
        pass

    def test_reset_password(self):
        pass

    def _test_create(self, data, **kwargs):
        self.setUpAuthentication()
        self.assertForbidden(self.client.post(self.list_url))

        self.client.logout()

        data_ = super()._test_create(data, **kwargs)
        self.check_user(data_)
        media_path = urlparse(settings.MEDIA_URL).path.strip("/")
        avatar_path = urlparse(data_.pop("avatar")).path.strip("/")
        avatar = "/".join(avatar_path.split("/")[len(media_path.split("/")):])
        data_.update({"avatar": avatar})
        self.assertTrue(get_user_model().objects.filter(**data_).exists())
        self.assertTrue(default_storage.exists(avatar))
        default_storage.delete(avatar)

    def check_user(self, user):
        self.assertIsInstance(user, dict)
        keys = [
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
        ]
        self.assertEqual(list(user.keys()), keys)
