from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.shortcuts import loader

from base_django_rest_framework.managers import UserManager
from base_django_rest_framework.signing import UserSigner
from .mixins import UUIDMixin, CreatedAtMixin, UpdatedAtMixin


class User(UUIDMixin, CreatedAtMixin, UpdatedAtMixin, AbstractUser):
    avatar = models.ImageField(upload_to="users/avatars", blank=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    date_joined = None

    REQUIRED_FIELDS = ["first_name", "last_name"]

    if settings.INCLUDE_USERNAME_COLUMN:
        REQUIRED_FIELDS.insert(0, "email")
    else:
        username = None
        USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        ordering = ["-created_at"]

    def get_signature(self, **kwargs):
        return UserSigner.sign({"user": {"id": str(self.id)}, "extra": kwargs})

    def verify(self, is_verified):
        self.is_verified = is_verified
        self.save()

    def update_password(self, password):
        self.set_password(password)
        self.save()

    def email_user(self, subject, message, from_email=None, **kwargs):
        to_email = kwargs.pop("to_email")
        if to_email is None:
            to_email = self.email
        send_mail(
            subject,
            message,
            from_email,
            [f"{self.get_full_name()} <{to_email}>"],
            **kwargs)

    def send_action_email(self, subject, context, to_email=None):
        context.setdefault("theme", "")
        context.update({"title": subject, "user": self.get_short_name()})
        self.email_user(
            subject,
            loader.render_to_string("base_django_rest_framework/action.txt", context),
            html_message=loader.render_to_string("base_django_rest_framework/action.html", context),
            to_email=to_email
        )

    def send_email_confirmation_link(self, email=None):
        if email is None:
            action_link = settings.EMAIL_CONFIRMATION_URL.format(signature=self.get_signature())
        else:
            action_link = settings.EMAIL_CHANGE_URL.format(signature=self.get_signature(email=email))
        self.send_action_email(
            "Email Confirmation",
            {
                "action": "Confirm Your Email Address",
                "action_text": "Confirm Email Address",
                "action_link": action_link
            },
            to_email=email
        )

    def send_password_reset_link(self):
        self.send_action_email(
            "Password Reset",
            {
                "theme": "yellow",
                "action": "Reset Your Password",
                "action_text": "Reset Password",
                "action_link": settings.PASSWORD_RESET_URL.format(signature=self.get_signature())
            }
        )
