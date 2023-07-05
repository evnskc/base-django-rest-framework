from django.contrib.admin import register, display
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as _UserAdmin


@register(get_user_model())
class UserAdmin(_UserAdmin):
    fieldsets = (
        (None, {"fields": ("id",)}),
        ("Personal info", {"fields": ("avatar", "first_name", "last_name", "username", "email")}),
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
    add_fieldsets = ((None, {"classes": ("wide",),
                             "fields": ("first_name", "last_name", "username", "email", "password1", "password2")},),)
    list_display = ("full_name", "username", "email", "is_verified", "created_at")
    list_filter = ("is_verified", "is_active", "is_staff", "is_superuser", "groups")
    search_fields = ("first_name", "last_name", "username", "email")
    readonly_fields = ("id", "created_at", "updated_at", "last_login")
    ordering = ("-created_at",)

    @display(description="full name")
    def full_name(self, instance):
        return instance.get_full_name()
