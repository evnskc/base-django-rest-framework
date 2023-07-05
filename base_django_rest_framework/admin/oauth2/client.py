from datetime import datetime

from django.contrib.admin import SimpleListFilter, ModelAdmin, register, display

from base_django_rest_framework.models import OAuth2Client


class ClientSecretStatusFilter(SimpleListFilter):
    title = "client secret status"

    parameter_name = "client_secret_status"

    def lookups(self, request, model_admin):
        return ("active", "Active"), ("expired", "Expired")

    def queryset(self, request, queryset):
        return queryset.filter(client_secret_is_expired=self.value() == "expired")


@register(OAuth2Client)
class OAuth2ClientAdmin(ModelAdmin):
    fieldsets = (
        (None, {"fields": (
            "id",
            "client_id",
            "client_secret",
            "client_name",
            "redirect_uris",
            "default_redirect_uri",
            "scope",
            "response_type",
            "grant_type",
            "token_endpoint_auth_method")}),
        ("Important dates", {"fields": ("client_id_issued_at", "client_secret_expires_at")}),
    )
    list_display = ("client_name", "client_secret_is_active", "client_id_issued_at_datetime")
    list_filter = (ClientSecretStatusFilter,)
    search_fields = ("client_id", "client_name")
    readonly_fields = ("id", "client_id", "client_secret", "client_id_issued_at", "client_secret_expires_at")
    ordering = ("-client_id_issued_at",)

    @display(description="client secret is active", boolean=True)
    def client_secret_is_active(self, instance):
        return not getattr(instance, "client_secret_is_expired")

    @display(description="client id issued at")
    def client_id_issued_at_datetime(self, instance):
        return datetime.fromtimestamp(instance.client_id_issued_at)
