from django.core.management.base import BaseCommand, CommandParser

from afauth.models import AFUser


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--email", "-e", type=str)
        parser.add_argument("--password", "-p", type=str)

    def handle(self, *args, **options):
        if "email" not in options or "password" not in options:
            return

        email = options["email"]
        password = options["password"]

        if not AFUser.objects.filter(email=email):
            AFUser.objects.create_superuser(email=email, first_name="admin", last_name="admin", password=password)
