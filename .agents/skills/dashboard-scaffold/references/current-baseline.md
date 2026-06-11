# Current Baseline Checklist

Use this checklist when reproducing the current Kisomo-style scaffold.

## Core Files

- `pyproject.toml`
- `requirements.lock`
- `.env.example`
- `docker-compose.yml`
- `init.sh`
- `manage.py`
- `config/settings.py`
- `config/urls.py`
- `config/asgi.py`
- `config/wsgi.py`
- `config/celery.py`
- `scripts/local_preview.sh`
- `scripts/validate_json.py`

## Apps

- `apps/__init__.py`
- `apps/users/models.py`
- `apps/users/managers.py`
- `apps/users/forms.py`
- `apps/users/views.py`
- `apps/users/services.py`
- `apps/users/roles.py`
- `apps/users/admin.py`
- `apps/users/tests.py`
- `apps/users/migrations/0001_initial.py`
- `apps/users/migrations/0002_userinvitation.py`

## Templates

- `templates/registration/login.html`
- `templates/registration/invite_accept.html`
- `templates/registration/logged_out.html`
- `templates/registration/profile.html`
- `templates/socialaccount/login.html`
- `templates/socialaccount/login_cancelled.html`
- `templates/base.html`
- `templates/app/base_page.html`
- `templates/app/page.html`
- `templates/users/index.html`
- `templates/users/invite_form.html`

## Static

- `static/dissertation/auth/auth.css`
- `static/dissertation/ui/tokens.css`
- `static/dissertation/ui/components.css`
- `static/dissertation/ui/authenticated.css`
- `static/dissertation/ui/shell.js`
- logo/auth assets under `static/img/`

## Shell Behavior

- left sidebar with logo
- routine nav at top
- configuration nav at bottom
- configuration label uses a standout accented tool icon badge
- collapsible drawer
- 64px topbar
- breadcrumbs
- topbar page title only
- notification icon
- account dropdown with icon-labeled actions
- only content pane scrolls on desktop

## Routes

- `/accounts/login/`
- `/accounts/google/login/`
- `/accounts/google/login/callback/`
- `/accounts/invite/new/`
- `/accounts/invite/<uid>/<token>/`
- `/users/`
- `/`

## Verification

- `./init.sh`
- `python manage.py migrate --noinput`
- `python manage.py test apps.users`
- `python scripts/validate_json.py`
