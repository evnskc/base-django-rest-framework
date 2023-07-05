from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation

from .model import ModelSerializer

_fields = [
    "id",
    "avatar",
    "first_name",
    "last_name",
    "username",
    "email",
    "password",
    "is_verified",
    "is_active",
    "is_staff",
    "is_superuser",
    "created_at",
    "updated_at"
]

_readonly_fields = [
    "id",
    "is_verified",
    "is_active",
    "is_staff",
    "is_superuser",
    "created_at",
    "updated_at"
]

_write_only_fields = ["password"]


class UserSerializer(ModelSerializer):
    def validate_password(self, value):
        user = self.instance
        if user is None:
            user = get_user_model()(**self.initial_data)
        password_validation.validate_password(value, user=user)
        return value

    class Meta:
        model = get_user_model()
        fields = _fields
        read_only_fields = _readonly_fields
        extra_kwargs = {
            "password": {"write_only": True}
        }


class UserUpdateSerializer(UserSerializer):
    def __init__(self, *args, fields=None, **kwargs):
        super().__init__(*args, fields=fields, **kwargs)
        self.fields.pop("password")

    class Meta(UserSerializer.Meta):
        read_only_fields = [*_readonly_fields, "email"]


class UserUpdateActiveStatusSerializer(UserUpdateSerializer):
    class Meta(UserUpdateSerializer.Meta):
        read_only_fields = [field for field in _fields if field not in [*_write_only_fields, "is_active"]]


class UserUpdateAdminStatusSerializer(UserUpdateSerializer):
    class Meta(UserUpdateSerializer.Meta):
        read_only_fields = [
            field for field in _fields if field not in [*_write_only_fields, "is_staff", "is_superuser"]
        ]


class UserUpdateEmailSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ["email"]
        extra_kwargs = {
            "email": {"write_only": True}
        }


class UserUpdatePasswordSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ["password"]
