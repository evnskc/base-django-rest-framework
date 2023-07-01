from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from base_django_rest_framework.permissions import IsSelf, IsSuperuser
from base_django_rest_framework.permissions import ModelPermissions
from base_django_rest_framework.serializers import (UserSerializer, UserUpdateSerializer, UserUpdateEmailSerializer,
                                                    UserUpdateActiveStatusSerializer,
                                                    UserUpdateAdminStatusSerializer, UserUpdatePasswordSerializer)
from base_django_rest_framework.signals import email_changed, password_changed
from base_django_rest_framework.signing import UserSigner
from base_django_rest_framework.throttles import CreateUserRateThrottle, EmailUserRateThrottle
from .model import ModelViewSet


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "user"
    lookup_url_converter = "uuid"

    def get_serializer(self, *args, **kwargs):
        if self.action in (self.update.__name__, self.partial_update.__name__):
            self.serializer_class = UserUpdateSerializer
        elif self.action == self.update_email_link.__name__:
            self.serializer_class = UserUpdateEmailSerializer
        elif self.action == self.update_active_status.__name__:
            self.serializer_class = UserUpdateActiveStatusSerializer
        elif self.action == self.update_admin_status.__name__:
            self.serializer_class = UserUpdateAdminStatusSerializer
        elif self.action in (self.update_password.__name__, self.reset_password.__name__):
            self.serializer_class = UserUpdatePasswordSerializer
        else:
            self.serializer_class = UserSerializer
        return super().get_serializer(*args, **kwargs)

    @action(methods=["get"], detail=False, url_path="email/update/<str:signature>", url_name="email-update")
    def update_email(self, request, *args, **kwargs):
        user, extra = UserSigner.unsign(self.kwargs["signature"], 3600)
        user.email = extra["email"]
        user.save()
        email_changed.send(sender=user.__class__, instance=user)
        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=["post"], detail=False, url_path="email/update", url_name="email-update-link")
    def update_email_link(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.send_email_change_link(serializer.validated_data["email"])
        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=["get"], detail=False, url_path="email/verify/<str:signature>", url_name="email-verify")
    def verify_email(self, request, *args, **kwargs):
        user, extra = UserSigner.unsign(self.kwargs["signature"], 3600)
        user.verify(True)
        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=["get"], detail=False, url_path="email/verify", url_name="email-verify-link")
    def verify_email_link(self, request, *args, **kwargs):
        if not request.user.is_verified:
            request.user.send_email_confirmation_link()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=["patch"], detail=True, url_path="active/update", url_name="active-update")
    def update_active_status(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @action(methods=["patch"], detail=True, url_path="admin/update", url_name="admin-update")
    def update_admin_status(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @action(methods=["post"], detail=False, url_path="password/update", url_name="password-update")
    def update_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.update_password(serializer.validated_data["password"])
        password_changed.send(request.user.__class__, instance=request.user)
        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=["post"], detail=False, url_path="password/reset/<str:signature>", url_name="password-reset")
    def reset_password(self, request, *args, **kwargs):
        user, extra = UserSigner.unsign(self.kwargs["signature"], 3600)
        serializer = self.get_serializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.update_password(serializer.validated_data["password"])
        password_changed.send(user.__class__, instance=user)
        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=["post"], detail=False, url_path="password/reset", url_name="password-reset-link")
    def reset_password_link(self, request, *args, **kwargs):
        email = request.POST["email"]
        user = get_object_or_404(get_user_model(), email=email)
        user.send_email_verification_link(email)
        return Response(status=HTTP_204_NO_CONTENT)

    def get_throttles(self):
        throttles = super().get_throttles()
        if self.action == self.create.__name__:
            throttles.extend([throttle() for throttle in [CreateUserRateThrottle]])
        if self.action in (
                self.update_email_link.__name__,
                self.verify_email_link.__name__,
                self.reset_password_link.__name__):
            throttles.extend([throttle() for throttle in [EmailUserRateThrottle]])
        return throttles

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.action == self.create.__name__:
            permissions.extend([permission() for permission in [~IsAuthenticated]])
        if self.action in (
                self.list.__name__,
                self.retrieve.__name__,
                self.update.__name__,
                self.partial_update.__name__,
                self.destroy.__name__,
                self.update_email_link.__name__,
                self.verify_email_link.__name__,
                self.update_password.__name__,
                self.update_active_status.__name__,
                self.update_admin_status.__name__):
            permissions.extend([permission() for permission in [IsAuthenticated]])
        if self.action == self.list.__name__:
            permissions.extend([permission() for permission in [ModelPermissions]])
        if self.action in (
                self.retrieve.__name__,
                self.update.__name__,
                self.partial_update.__name__,
                self.destroy.__name__):
            permissions.extend([permission() for permission in [IsSelf | ModelPermissions]])
        if self.action == self.update_active_status.__name__:
            permissions.extend([permission() for permission in [~IsSelf & ModelPermissions]])
        if self.action == self.update_admin_status.__name__:
            permissions.extend([permission() for permission in [~IsSelf & IsSuperuser]])
        if self.action in (self.reset_password.__name__, self.reset_password_link.__name__):
            permissions.extend([permission() for permission in [~IsAuthenticated]])
        return permissions
