.PHONY: help install dev test lint format docker-up docker-down db-migrate seed

help: ## Display this help message
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies for API and Web
	cd api && uv pip install -e .[dev]
	cd web && pnpm install

dev: ## Start development servers locally
	@echo "Starting development servers..."
	# In a real setup you might use a tool like overmind or just rely on docker-compose for dev
	docker-compose up

test: ## Run all tests
	cd api && pytest
	cd web && pnpm test

lint: ## Run linters
	cd api && ruff check .
	cd web && pnpm lint

format: ## Run formatters
	cd api && ruff format .
	cd web && pnpm format

docker-up: ## Start all services with Docker Compose
	docker-compose up -d

docker-down: ## Stop all Docker Compose services
	docker-compose down

db-migrate: ## Run database migrations
	docker-compose exec api alembic upgrade head

seed: ## Seed the database with initial data
	docker-compose exec api python scripts/seed.py
