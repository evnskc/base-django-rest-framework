import time

from django.db.models import Manager, Case, When, Q, F


class OAuth2TokenManager(Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            expires_at=F("issued_at") + F("expires_in"),
            is_expired_=Case(When(Q(expires_in=0) | Q(expires_at__gt=time.time()), then=False), default=True)
        )
