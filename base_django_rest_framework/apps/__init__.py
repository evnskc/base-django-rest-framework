from django.apps import AppConfig


class BaseDjangoRestFrameworkConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "base_django_rest_framework"
    verbose_name = "Base Django Rest Framework"

    def ready(self):
        from base_django_rest_framework import signals  # NOQA
