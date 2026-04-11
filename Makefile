.PHONY: setup dev stop test lint format migrate

setup: ## First-time setup: start DB, install deps, run migrations
	docker compose up -d db
	uv sync
	uv run pre-commit install
	uv run python manage.py migrate

dev: ## Start DB and run dev server
	docker compose up -d db
	uv run python manage.py runserver

stop: ## Stop dev server and database
	-pkill -f "manage.py runserver" 2>/dev/null || true
	docker compose stop db

test: ## Run tests
	uv run pytest

lint: ## Run linter and formatter check
	uv run ruff check .
	uv run ruff format --check .

format: ## Auto-fix lint and formatting
	uv run ruff check --fix .
	uv run ruff format .

migrate: ## Create and apply migrations
	uv run python manage.py makemigrations
	uv run python manage.py migrate
