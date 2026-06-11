from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()

    def clean(self) -> None:
        super().clean()
        if self.email:
            self.email = self.__class__.objects.normalize_email(self.email).lower()

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.__class__.objects.normalize_email(self.email).lower()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["email"]

    def __str__(self) -> str:
        return self.get_full_name() or self.email


class UserInvitation(models.Model):
    class Status(models.TextChoices):
        PENDING = "Pending", "Pending"
        ACCEPTED = "Accepted", "Accepted"
        REVOKED = "Revoked", "Revoked"
        EXPIRED = "Expired", "Expired"

    email = models.EmailField()
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    role_key = models.CharField(max_length=80)
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING,
    )
    token_digest = models.CharField(max_length=64, unique=True)
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="sent_user_invitations",
    )
    invited_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    accepted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="accepted_user_invitations",
        null=True,
        blank=True,
    )
    accepted_at = models.DateTimeField(null=True, blank=True)
    revoked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="revoked_user_invitations",
        null=True,
        blank=True,
    )
    revoked_at = models.DateTimeField(null=True, blank=True)
    last_sent_at = models.DateTimeField(null=True, blank=True)
    resend_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-invited_at", "-id"]
        constraints = [
            models.UniqueConstraint(
                fields=["email"],
                condition=models.Q(status="Pending"),
                name="unique_pending_user_invitation_email",
            ),
        ]

    def save(self, *args, **kwargs):
        if self.email:
            self.email = BaseUserManager.normalize_email(self.email).lower()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.email} invitation"
