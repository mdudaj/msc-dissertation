# Session Progress Log

## Current State

**Last Updated:** 2026-06-09
**Active Feature:** feat-001 - Reproducible Topic Brief Run Review Gate

## Done

- [x] Normalized Kisomo image assets under `static/img/`.
- [x] Exported PNG assets for auth background, brand, muted hero, and Google mark.
- [x] Added Django project scaffold.
- [x] Added custom email-based user model and admin/forms/management command.
- [x] Added Google OAuth2 configuration through `django-allauth`.
- [x] Added left-panel Google-only login template.
- [x] Added separated dissertation auth/authenticated UI CSS layers.
- [x] Verified the baseline harness with `./init.sh`.
- [x] Applied baseline migrations with `python manage.py migrate --noinput`.
- [x] Verified focused auth/user behavior with `python manage.py test apps.users`.
- [x] Validated feature tracking JSON with `python scripts/validate_json.py`.
- [x] Verified the login page responds with `200 OK` at `/accounts/login/`
      on the local dev server.
- [x] Restored local email/password login below Google sign-in for superuser
      recovery and invite-created accounts.
- [x] Added governed user invitations with Research Operator and Evaluator
      roles, superuser-only invite creation, and invite acceptance.
- [x] Copied the relevant Google OAuth environment keys from the old
      dissertation `.env` into this workspace `.env` without carrying old
      database assumptions.
- [x] Verified `/accounts/google/login/` redirects to Google using the copied
      OAuth configuration.
- [x] Fixed `scripts/local_preview.sh` so `prep` waits for a real Postgres
      connection before migrations, `dev` prepares services before serving, and
      `down/status/logs/urls` are supported.
- [x] Replaced the authenticated Viewflow default page shell with a Kisomo-owned
      shell: side navigation, top bar, Dashboard, and Configuration / Users &
      Roles.

## In Progress

- [ ] Review whether to restore the old dissertation curriculum/topic-brief
      workflows as-is or refactor them into the new harness structure first.

## Next Review

- [ ] Decide the restoration posture for feat-001 before copying curriculum,
      experiments, artifacts, or async workflow code.
