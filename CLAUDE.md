# CLAUDE.md — Project Conventions

## Project
Monitoring and curation platform with data/ML pipeline. Django API backend, React frontend (separate repo), PostgreSQL 16.

## Commands (via Makefile)
- **First-time setup**: `make setup` (start DB + install deps + migrate)
- **Dev server**: `make dev` (start DB + runserver)
- **Run tests**: `make test`
- **Lint check**: `make lint`
- **Auto-fix lint/format**: `make format`
- **Migrations**: `make migrate`

## Structure
- `config/` — Django project (settings, urls, wsgi, asgi)
- `config/settings/` — Split settings: `base.py`, `dev.py`, `prod.py`
- `apps/` — Django apps with `apps.` prefix (e.g., `apps.core`)
- `.specs/` — Project documentation and specs

## Conventions
- **TDD mandatory** — write tests before implementation
- **Settings module**: `config.settings.dev` (dev), `config.settings.prod` (prod)
- **App creation**: `uv run django-admin startapp <name> apps/<name>`, then set `name = "apps.<name>"` in apps.py
- **Language**: Code and commits in English, documentation may be in Portuguese
- **Linter/formatter**: ruff (configured in pyproject.toml)
- **Package manager**: uv (never use pip directly)
- **Tests**: pytest-django, test files in `apps/<name>/tests/`

## Deploy (Render)
- **Build command**: `./build.sh`
- **Start command**: `gunicorn config.wsgi:application`
- **Env vars**: `SECRET_KEY`, `DATABASE_URL`, `DJANGO_SETTINGS_MODULE=config.settings.prod`, `ALLOWED_HOSTS`
