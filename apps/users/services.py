from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.users.models import UserInvitation
from apps.users.roles import assign_dissertation_role
from apps.users.roles import role_for_key
from apps.users.roles import seed_dissertation_roles


DEFAULT_INVITE_TTL = timedelta(days=7)


@dataclass(frozen=True)
class InviteToken:
    invitation: UserInvitation
    token: str


def create_user_invitation(
    *,
    email: str,
    first_name: str,
    last_name: str,
    role_key: str,
    invited_by,
    ttl: timedelta = DEFAULT_INVITE_TTL,
) -> InviteToken:
    if not getattr(invited_by, "is_superuser", False):
        raise ValidationError("only superusers can create invitations.")
    normalized_email = _normalize_email(email)
    _validate_role_key(role_key)
    _validate_invite_email(normalized_email)
    token = secrets.token_urlsafe(32)
    now = timezone.now()
    invitation = UserInvitation.objects.create(
        email=normalized_email,
        first_name=first_name.strip(),
        last_name=last_name.strip(),
        role_key=role_key,
        token_digest=digest_invite_token(token),
        invited_by=invited_by,
        invited_at=now,
        expires_at=now + ttl,
        last_sent_at=now,
    )
    return InviteToken(invitation=invitation, token=token)


def accept_user_invitation(
    *,
    invitation: UserInvitation,
    token: str,
    password: str,
) -> UserInvitation:
    invitation = UserInvitation.objects.get(pk=invitation.pk)
    _validate_pending_token(invitation, token)
    with transaction.atomic():
        invitation = UserInvitation.objects.select_for_update().get(pk=invitation.pk)
        _validate_pending_token(invitation, token)
        User = get_user_model()
        user = User.objects.filter(email=invitation.email).first()
        if user is None:
            user = User(
                email=invitation.email,
                first_name=invitation.first_name,
                last_name=invitation.last_name,
                is_active=True,
            )
        elif user.is_active:
            raise ValidationError("invited account is already active.")
        else:
            user.first_name = invitation.first_name
            user.last_name = invitation.last_name
            user.is_active = True
        validate_password(password, user)
        user.set_password(password)
        user.save()
        seed_dissertation_roles()
        assign_dissertation_role(user, invitation.role_key)
        invitation.status = UserInvitation.Status.ACCEPTED
        invitation.accepted_by = user
        invitation.accepted_at = timezone.now()
        invitation.save(update_fields=["status", "accepted_by", "accepted_at"])
        return invitation


def digest_invite_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _validate_pending_token(invitation: UserInvitation, token: str) -> None:
    if invitation.status != UserInvitation.Status.PENDING:
        raise ValidationError("invitation is not pending.")
    if invitation.expires_at <= timezone.now():
        invitation.status = UserInvitation.Status.EXPIRED
        invitation.save(update_fields=["status"])
        raise ValidationError("invitation has expired.")
    if not secrets.compare_digest(invitation.token_digest, digest_invite_token(token)):
        raise ValidationError("invitation token is invalid.")


def _validate_invite_email(email: str) -> None:
    User = get_user_model()
    if User.objects.filter(email=email, is_active=True).exists():
        raise ValidationError("user email is already active.")
    if UserInvitation.objects.filter(
        email=email,
        status=UserInvitation.Status.PENDING,
    ).exists():
        raise ValidationError("user email already has a pending invitation.")


def _normalize_email(email: str) -> str:
    if not email:
        raise ValidationError("email is required.")
    return get_user_model().objects.normalize_email(email).lower()


def _validate_role_key(role_key: str) -> None:
    try:
        role_for_key(role_key)
    except ValueError as exc:
        raise ValidationError(str(exc)) from exc
