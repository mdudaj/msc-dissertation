from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import DissertationUserChangeForm
from .forms import DissertationUserCreationForm
from .models import User
from .models import UserInvitation


@admin.register(User)
class DissertationUserAdmin(UserAdmin):
    add_form = DissertationUserCreationForm
    form = DissertationUserChangeForm
    model = User
    ordering = ("email",)
    list_display = ("email", "first_name", "last_name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "is_superuser", "groups")
    search_fields = ("email", "first_name", "last_name")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


@admin.register(UserInvitation)
class UserInvitationAdmin(admin.ModelAdmin):
    list_display = ("email", "role_key", "status", "invited_by", "invited_at", "expires_at")
    list_filter = ("status", "role_key")
    search_fields = ("email", "first_name", "last_name")
    readonly_fields = (
        "token_digest",
        "invited_by",
        "invited_at",
        "accepted_by",
        "accepted_at",
        "revoked_by",
        "revoked_at",
        "last_sent_at",
        "resend_count",
    )
