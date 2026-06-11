---
name: dashboard-scaffold
description: "Create a minimal Django dashboard scaffold like the current Kisomo baseline: custom email user, Google OAuth, invite/local-login auth flow, owned LIMS-like shell with side nav/topbar/account menu, dashboard page, Users & Roles configuration page, static assets, preview script, and verification. Use when the user asks to scaffold, bootstrap, cookiecutter, or reproduce this auth/dashboard harness in a repo."
---

# Dashboard Scaffold

Use this skill to create a working minimal auth/dashboard harness similar to
the Kisomo baseline in this repository.

## What This Skill Should Produce

A scaffolded repo should include:

- Django project config
- custom email-based user model
- Google OAuth via `django-allauth`
- local email/password login retained for superusers and invite-created users
- governed invite acceptance flow
- owned authenticated shell, not Viewflow default chrome
- LIMS-like side navigation and topbar
- bottom-pinned Configuration section with a standout accented tool icon badge
- Dashboard page
- Configuration / Users & Roles page
- separated auth and authenticated CSS layers
- `init.sh`, `scripts/local_preview.sh`, `.env.example`, `docker-compose.yml`
- focused user/auth/shell tests

See `references/current-baseline.md` for the exact target checklist.

## Required Inputs

Ask for missing values before editing:

- product name, e.g. `Kisomo`
- primary color
- secondary color
- accent color
- logo/static image source path
- allowed OAuth provider(s), default `google`
- desired local preview port, default `8000`
- design variant:
  - `Operational`: closest to LIMS
  - `Educational Research`: Kisomo default
  - `Executive Overview`: more KPI-forward

If the user says “use this repo/current scaffold,” infer these values from the
current files and proceed.

## Workflow

1. Inspect the target repo state with `find`, `rg`, and existing settings.
2. Decide whether this is a fresh scaffold or a retrofit.
3. Preserve user changes. Do not delete unrelated files.
4. Create or update the baseline files listed in `references/current-baseline.md`.
5. Add tests that assert:
   - login renders local form and Google action
   - invite acceptance creates a user
   - authenticated pages use owned shell classes
   - pages do not include Viewflow default menu chrome
   - page titles follow `<Product> | <Page Title>`
6. Run:

```bash
./init.sh
python manage.py migrate --noinput
python manage.py test apps.users
python scripts/validate_json.py
```

## Script Policy

This should become a script-backed scaffold skill when reused across repos.
Follow Agent Skills guidance:

- keep `SKILL.md` concise
- put detailed file inventory in `references/`
- put deterministic generators in `scripts/`
- scripts must be non-interactive
- scripts must support `--help`
- scripts should be idempotent and safe to rerun
- prefer `--dry-run` before writing files

Recommended script shape:

```bash
python scripts/scaffold.py \
  --product Kisomo \
  --variant educational-research \
  --primary '#0b4f76' \
  --secondary '#0b6e6e' \
  --accent '#f4c542' \
  --target .
```

Do not build a fragile script until the current scaffold stabilizes. For the
first pass, implement by patching files directly and keep this skill as the
checklist. Add `scripts/scaffold.py` once a second repo needs the same scaffold.
