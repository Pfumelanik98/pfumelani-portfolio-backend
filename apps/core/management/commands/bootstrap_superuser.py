import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


ENVIRONMENT_VARIABLES = {
    "DJANGO_BOOTSTRAP_SUPERUSER": "true",
    "DJANGO_BOOTSTRAP_SUPERUSER_USERNAME": None,
    "DJANGO_BOOTSTRAP_SUPERUSER_EMAIL": None,
    "DJANGO_BOOTSTRAP_SUPERUSER_PASSWORD": None,
}


class Command(BaseCommand):
    help = "Create an initial superuser from explicitly enabled environment variables."

    def handle(self, *args, **options):
        configured = {
            name: os.environ.get(name)
            for name in ENVIRONMENT_VARIABLES
            if name in os.environ
        }
        if not configured:
            self.stdout.write("Superuser bootstrap not requested; no account changes made.")
            return

        missing = set(ENVIRONMENT_VARIABLES) - configured.keys()
        if missing:
            raise CommandError(
                "Incomplete superuser bootstrap configuration. Missing: "
                + ", ".join(sorted(missing))
            )

        if configured["DJANGO_BOOTSTRAP_SUPERUSER"].lower() != "true":
            raise CommandError(
                "Set DJANGO_BOOTSTRAP_SUPERUSER to 'true' to explicitly enable bootstrap."
            )

        username = configured["DJANGO_BOOTSTRAP_SUPERUSER_USERNAME"].strip()
        email = configured["DJANGO_BOOTSTRAP_SUPERUSER_EMAIL"].strip()
        password = configured["DJANGO_BOOTSTRAP_SUPERUSER_PASSWORD"]
        if not username or not email or not password:
            raise CommandError("Bootstrap username, email, and password must not be empty.")

        user_model = get_user_model()
        username_field = user_model.USERNAME_FIELD
        candidate = user_model(**{username_field: username})
        if any(field.name == "email" for field in user_model._meta.fields):
            candidate.email = email

        try:
            validate_email(email)
            validate_password(password, user=candidate)
        except ValidationError as error:
            raise CommandError("; ".join(error.messages)) from error

        manager = user_model._default_manager
        if manager.filter(**{username_field: username}).exists():
            raise CommandError(
                "A user with that username already exists; no account changes were made."
            )

        manager.db_manager().create_superuser(
            **{
                username_field: username,
                "email": email,
                "password": password,
            }
        )
        self.stdout.write("Initial production superuser created.")
