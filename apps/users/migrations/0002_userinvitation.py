# Generated for the Kisomo baseline invite flow.

import django.db.models.deletion
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserInvitation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("email", models.EmailField(max_length=254)),
                ("first_name", models.CharField(max_length=150)),
                ("last_name", models.CharField(max_length=150)),
                ("role_key", models.CharField(max_length=80)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Pending", "Pending"),
                            ("Accepted", "Accepted"),
                            ("Revoked", "Revoked"),
                            ("Expired", "Expired"),
                        ],
                        default="Pending",
                        max_length=16,
                    ),
                ),
                ("token_digest", models.CharField(max_length=64, unique=True)),
                ("invited_at", models.DateTimeField()),
                ("expires_at", models.DateTimeField()),
                ("accepted_at", models.DateTimeField(blank=True, null=True)),
                ("revoked_at", models.DateTimeField(blank=True, null=True)),
                ("last_sent_at", models.DateTimeField(blank=True, null=True)),
                ("resend_count", models.PositiveIntegerField(default=0)),
                (
                    "accepted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="accepted_user_invitations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "invited_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="sent_user_invitations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "revoked_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="revoked_user_invitations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-invited_at", "-id"],
            },
        ),
        migrations.AddConstraint(
            model_name="userinvitation",
            constraint=models.UniqueConstraint(
                condition=models.Q(("status", "Pending")),
                fields=("email",),
                name="unique_pending_user_invitation_email",
            ),
        ),
    ]
