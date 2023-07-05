from django.contrib.auth.models import UserManager as _UserManager


class UserManager(_UserManager):
    def create(self, **kwargs):
        return self.create_user(**kwargs)

    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        return super()._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        return super().create_superuser(username, email, password, is_verified=True, **extra_fields)
