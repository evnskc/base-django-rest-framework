from django.conf import settings
from django.contrib.admin import register, display
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as _UserAdmin


@register(get_user_model())
class UserAdmin(_UserAdmin):
    fieldsets = (
        (None, {"fields": ("id", "username")}),
        ("Personal info", {"fields": ("avatar", "first_name", "last_name", "email")}),
        ("Permissions", {
            "fields": (
                "is_verified",
                "is_active",
                "is_staff",
                "is_superuser",
                "user_permissions",
                "groups"
            )
        }),
        ("Important dates", {"fields": ("created_at", "updated_at", "last_login")}),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("username", "password1", "password2")},),)
    list_display = ("full_name", "username", "email", "is_verified", "created_at")
    list_filter = ("is_verified", "is_active", "is_staff", "is_superuser", "groups")
    search_fields = ("first_name", "last_name", "username", "email")
    readonly_fields = ("id", "created_at", "updated_at", "last_login")
    ordering = ("-created_at",)

    @display(description="full name")
    def full_name(self, instance):
        return instance.get_full_name()

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        if not settings.INCLUDE_USERNAME_COLUMN:
            self.fieldsets[0][1].update(dict(fields=tuple(
                field if field != "username" else "email" for field in self.fieldsets[0][1]["fields"]
            )))
            self.fieldsets[1][1].update(dict(fields=tuple(
                field for field in self.fieldsets[1][1]["fields"] if field != "email"
            )))
            self.add_fieldsets[0][1].update(dict(fields=tuple(
                field if field != "username" else "email" for field in self.add_fieldsets[0][1]["fields"]
            )))
            self.list_display = tuple(field for field in self.list_display if field != "username")
            self.search_fields = tuple(field for field in self.search_fields if field != "username")
