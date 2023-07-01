from django.core.management.base import BaseCommand

from base_django_rest_framework.models import OAuth2Token


class Command(BaseCommand):
    help = "Used to delete revoked oAuth2 tokens"
    requires_migrations_checks = True

    def handle(self, *args, **options):
        deleted, row_count = OAuth2Token.objects.filter(revoked=True).delete()
        self.stdout.write(
            self.style.SUCCESS(f"Successfully deleted {row_count.get(getattr(OAuth2Token, '_meta').label, 0)} tokens.")
        )
