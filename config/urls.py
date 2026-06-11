from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include
from django.urls import path
from django.views.generic import TemplateView

from apps.users.views import DissertationLoginView
from apps.users.views import InviteAcceptanceView
from apps.users.views import UserInvitationCreateView
from apps.users.views import UsersRolesView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", DissertationLoginView.as_view(), name="login"),
    path(
        "accounts/invite/new/",
        UserInvitationCreateView.as_view(),
        name="invite-new",
    ),
    path(
        "accounts/invite/<int:uid>/<str:token>/",
        InviteAcceptanceView.as_view(),
        name="invite-accept",
    ),
    path("users/", login_required(UsersRolesView.as_view()), name="users-roles"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("allauth.urls")),
    path("", login_required(TemplateView.as_view(template_name="app/page.html")), name="dashboard"),
]
