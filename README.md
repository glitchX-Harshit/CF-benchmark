# CF Benchmark

CF Benchmark is a sales-intelligence evaluation platform for measuring the quality and effectiveness of sales responses, objection handling, and conversation progression. The platform evaluates seller responses against structured sales scenarios and produces deterministic, explainable scores rather than relying on a single subjective LLM score.

## Architecture Overview

The system is built as a monorepo with the following core components:

- **API**: A Python/FastAPI backend handling evaluation, scoring, and data management.
- **Web**: A Next.js frontend for the evaluation playground, dashboard, and analytics.
- **Evaluation Engine**: Independent Python engine for deterministic sales response scoring.
- **Database**: PostgreSQL for persistent storage of scenarios, evaluations, and benchmarks.
- **Cache/Queue**: Redis for task queuing and caching.

## Tech Stack

- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2 (async), Pydantic v2, uv
- **Frontend**: Node 20, Next.js 14, TypeScript, Tailwind CSS, shadcn/ui, pnpm
- **Infrastructure**: Docker, Docker Compose, PostgreSQL 16, Redis 7
- **Testing**: Pytest, Vitest, Playwright
- **Tooling**: Ruff, MyPy, ESLint, Prettier

## Project Structure

```text
CF-Benchmark/
├── apps/
│   └── web/              # Next.js frontend application
├── services/
│   └── api/              # FastAPI backend service
│       └── app/
│           ├── api/          # Route handlers
│           ├── core/         # Middleware, exceptions, logging
│           ├── db/           # Database session management
│           ├── models/       # SQLAlchemy models
│           ├── schemas/      # Pydantic schemas
│           ├── services/     # Business logic
│           ├── repositories/ # Data access layer
│           └── evaluation/   # Evaluation engine (independent)
├── packages/             # Shared packages and contracts
├── data/                 # Benchmark data, scenarios, rubrics
│   ├── benchmarks/
│   ├── scenarios/
│   ├── rubrics/
│   ├── responses/
│   ├── fixtures/
│   └── golden/
├── docs/                 # Documentation
│   ├── architecture/
│   ├── evaluation/
│   └── decisions/
├── infra/                # Docker, PostgreSQL, Redis configs
├── scripts/              # Utility scripts
├── tests/                # Cross-service tests
├── docker-compose.yml
├── Makefile
└── .env.example
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repo-url> CF-Benchmark
   cd CF-Benchmark
   ```

2. **Environment Variables:**
   Copy the example environment file and configure it if necessary:
   ```bash
   cp .env.example .env
   ```

3. **Install Dependencies (Optional for local dev):**
   ```bash
   make install
   ```

4. **Start the Application:**
   To run everything via Docker Compose:
   ```bash
   make docker-up
   ```
   The API will be available at `http://localhost:8000` and the Web interface at `http://localhost:3000`.

## Development Commands

We use a `Makefile` to simplify common development tasks.

- `make install`: Install dependencies for both API and Web locally.
- `make dev` / `make docker-up`: Start the development environment.
- `make docker-down`: Stop the development environment.
- `make test`: Run all tests (API and Web).
- `make lint`: Run linters.
- `make format`: Run code formatters.
- `make db-migrate`: Run database migrations.
- `make seed`: Seed the database with initial development data.
