# ClozFlow

ClozFlow is a sales intelligence platform focused on understanding sales conversations, evaluating seller responses, and analyzing objection handling through the **CF Benchmark** system.

## Architecture

This is a Turborepo monorepo containing:
- `apps/web`: Next.js frontend (App Router, Tailwind)
- `apps/api`: FastAPI backend
- `packages/evaluation-engine`: Python library for deterministic and LLM-based rubric scoring.
- `packages/*`: Shared configurations and types.

## Local Setup

### Prerequisites
- Node.js >= 18
- pnpm
- Python >= 3.10
- Docker Desktop

### 1. Environment
Copy `.env.example` to `.env` in `apps/api` and root.

### 2. Infrastructure
Start the database and redis:
```bash
docker-compose up -d
```

### 3. Frontend
```bash
pnpm install
pnpm dev
```

### 4. Backend
```bash
python -m venv .venv
# Activate venv (.venv\Scripts\Activate.ps1 or source .venv/bin/activate)
pip install -e packages/evaluation-engine
pip install -e apps/api
cd apps/api
uvicorn app.main:app --reload --port 8000
```
