# CLAUDE.md — Project Conventions

## Project
Monitoring and curation platform with data/ML pipeline. Django API backend, React frontend (separate repo), PostgreSQL 16.

## Commands
- **Start DB**: `docker compose up -d db`
- **Run server**: `uv run python manage.py runserver`
- **Run tests**: `uv run pytest`
- **Run linter**: `uv run ruff check .`
- **Run formatter**: `uv run ruff format .`
- **Migrations**: `uv run python manage.py makemigrations && uv run python manage.py migrate`

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
