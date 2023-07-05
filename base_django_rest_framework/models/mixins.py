from uuid import uuid4

from django.db import models


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class CreatedAtMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        abstract = True


class UpdatedAtMixin(models.Model):
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True
