from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as _UserManager


class UserManager(_UserManager):

    def create(self, **kwargs):
        return self.create_user(**kwargs)

    def _create_user(self, username, email, password, **kwargs):
        kwargs.update({
            "email": self.normalize_email(email),
            "password": make_password(password)
        })
        if settings.INCLUDE_USERNAME_COLUMN:
            kwargs.update({"username": self.model.normalize_username(username)})
        return super().create(**kwargs)

    def create_superuser(self, username, email=None, password=None, **kwargs):
        kwargs.update({"is_verified": True})
        return super().create_superuser(username, email, password, **kwargs)
