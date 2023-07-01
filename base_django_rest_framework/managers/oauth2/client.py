import time

from django.db.models import Manager, Case, When, Q


class OAuth2ClientManager(Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            client_secret_is_expired=Case(
                When(Q(client_secret_expires_at=0) | Q(client_secret_expires_at__gt=time.time()), then=False),
                default=True
            )
        )
