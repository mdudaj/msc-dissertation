from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm

from .models import User
from .roles import ROLE_CATALOG
from .services import create_user_invitation


class DissertationAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "placeholder": "admin@example.com",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "placeholder": "Password",
            }
        ),
    )


class DissertationUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "first_name", "last_name")


class DissertationUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "is_superuser",
        )


class UserInvitationForm(forms.Form):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="First Name", max_length=150)
    last_name = forms.CharField(label="Last Name", max_length=150)
    role_key = forms.ChoiceField(
        label="Role",
        choices=[("", "Select role")] + [(role.key, role.label) for role in ROLE_CATALOG],
    )

    def save(self, *, invited_by):
        return create_user_invitation(
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            role_key=self.cleaned_data["role_key"],
            invited_by=invited_by,
        )


class InviteAcceptanceForm(SetPasswordForm):
    pass
