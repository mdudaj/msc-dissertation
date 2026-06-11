from __future__ import annotations

import getpass
import secrets

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    help = (
        "Create or update a superuser with friendlier email/password handling, "
        "including interactive retry and optional generated passwords."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "email",
            nargs="?",
            help="Superuser email address. If omitted in interactive mode, you will be prompted.",
        )
        parser.add_argument(
            "--email",
            dest="email_option",
            help="Superuser email address.",
        )
        parser.add_argument(
            "--password",
            dest="password",
            help="Password to set directly.",
        )
        parser.add_argument(
            "--generate-password",
            action="store_true",
            help="Generate a strong password and print it once after creation.",
        )
        parser.add_argument(
            "--noinput",
            action="store_true",
            help=(
                "Run non-interactively. If no password is provided, one will be generated "
                "and printed once."
            ),
        )

    def handle(self, *args, **options):
        email = self._resolve_email(
            positional_email=options.get("email"),
            option_email=options.get("email_option"),
            noinput=options["noinput"],
        )
        password, generated = self._resolve_password(
            explicit_password=options.get("password"),
            generate_password=options["generate_password"],
            noinput=options["noinput"],
        )

        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(email=email)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Superuser created: {email}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser updated: {email}"))

        if generated:
            self.stdout.write("Generated password (shown once):")
            self.stdout.write(password)

    def _resolve_email(
        self,
        *,
        positional_email: str | None,
        option_email: str | None,
        noinput: bool,
    ) -> str:
        provided_email = option_email or positional_email
        if positional_email and option_email and positional_email != option_email:
            raise CommandError("Provide the superuser email either positionally or with --email, not both.")

        while True:
            if provided_email:
                email = provided_email.strip().lower()
            elif noinput:
                raise CommandError("Provide a superuser email with --email or as a positional argument.")
            else:
                email = input("Superuser email: ").strip().lower()

            try:
                validate_email(email)
                return email
            except ValidationError:
                if provided_email or noinput:
                    raise CommandError("Provide a valid superuser email address.")
                self.stdout.write(self.style.ERROR("Enter a valid email address and try again."))

    def _resolve_password(
        self,
        *,
        explicit_password: str | None,
        generate_password: bool,
        noinput: bool,
    ) -> tuple[str, bool]:
        if explicit_password and generate_password:
            raise CommandError("Choose either --password or --generate-password, not both.")

        if explicit_password:
            self._validate_password(explicit_password)
            return explicit_password, False

        if generate_password or noinput:
            password = secrets.token_urlsafe(18)
            self._validate_password(password)
            return password, True

        while True:
            password = getpass.getpass("Password: ")
            password_confirm = getpass.getpass("Password (again): ")
            if password != password_confirm:
                self.stdout.write(self.style.ERROR("Passwords did not match. Try again."))
                continue
            try:
                self._validate_password(password)
                return password, False
            except CommandError as exc:
                self.stdout.write(self.style.ERROR(str(exc)))

    def _validate_password(self, password: str) -> None:
        try:
            validate_password(password)
        except ValidationError as exc:
            raise CommandError(" ".join(exc.messages)) from exc
