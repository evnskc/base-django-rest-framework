from django.core.management.base import BaseCommand

from base_django_rest_framework.models import OAuth2Client


class Command(BaseCommand):
    help = "Create an oAuth2 client"
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument(
            "--client_name",
            type=str,
            default="Default",
            help="default=\"Default\""
        )

    def handle(self, *args, **options):
        instance, created = OAuth2Client.objects.update_or_create(
            client_name=options.get("client_name"),
            grant_type="password refresh_token",
            token_endpoint_auth_method="none",
        )
        self.stdout.write(self.style.SUCCESS(
            f"Successfully created {instance.client_name} OAuth2 Client.\n"
            f"Client Id : {instance.client_id}\n"
            f"Client Secret : {instance.client_secret}\n"
            f"Grant Type : {instance.grant_type}\n"
            f"Token Endpoint Auth Method : {instance.token_endpoint_auth_method}"
        ))
