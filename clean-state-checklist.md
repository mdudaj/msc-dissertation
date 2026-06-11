# Clean State Checklist

- [x] `./init.sh` runs cleanly.
- [x] `python3 scripts/validate_json.py` passes.
- [x] `python manage.py check` passes.
- [x] `python manage.py migrate --noinput` applies migrations.
- [x] `./scripts/local_preview.sh prep` starts services, waits for Postgres, and applies migrations.
- [x] Login page renders with Kisomo assets and Google sign-in.
- [x] Curriculum/domain workflows remain pending review.
