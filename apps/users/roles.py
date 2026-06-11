from __future__ import annotations

from dataclasses import dataclass

from django.contrib.auth.models import Group


@dataclass(frozen=True)
class DissertationRole:
    key: str
    group_name: str
    label: str
    description: str


RESEARCH_OPERATOR = "research_operator"
EVALUATOR = "evaluator"

ROLE_CATALOG = (
    DissertationRole(
        key=RESEARCH_OPERATOR,
        group_name="Kisomo Research Operator",
        label="Research Operator",
        description="Configures workflows, inspects artifacts, and manages evidence.",
    ),
    DissertationRole(
        key=EVALUATOR,
        group_name="Kisomo Evaluator",
        label="Evaluator",
        description="Reviews assigned artifacts and submits feasibility feedback.",
    ),
)

ROLE_BY_KEY = {role.key: role for role in ROLE_CATALOG}
ROLE_GROUP_NAMES = tuple(role.group_name for role in ROLE_CATALOG)


def seed_dissertation_roles() -> list[Group]:
    groups = []
    for role in ROLE_CATALOG:
        group, _created = Group.objects.get_or_create(name=role.group_name)
        groups.append(group)
    return groups


def role_for_key(role_key: str) -> DissertationRole:
    try:
        return ROLE_BY_KEY[role_key]
    except KeyError as exc:
        raise ValueError(f"unknown dissertation role: {role_key}") from exc


def assign_dissertation_role(user, role_key: str) -> None:
    role = role_for_key(role_key)
    group, _created = Group.objects.get_or_create(name=role.group_name)
    user.groups.remove(*Group.objects.filter(name__in=ROLE_GROUP_NAMES))
    user.groups.add(group)


def user_role_keys(user) -> list[str]:
    if not getattr(user, "is_authenticated", False):
        return []
    names = set(user.groups.values_list("name", flat=True))
    return [role.key for role in ROLE_CATALOG if role.group_name in names]
