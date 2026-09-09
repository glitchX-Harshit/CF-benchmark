# ADR-001: Monorepo Architecture

## Context
We need to establish the repository structure for the CF Benchmark project, which includes a Python backend, a Next.js frontend, and various deployment configurations.

## Decision
We will use a Monorepo structure.

## Rationale
- **Simplified Setup**: A single repository allows developers to clone and run the entire stack with a single `docker-compose up`.
- **Atomic Commits**: Features requiring frontend and backend changes can be merged in a single PR.
- **Shared Tooling**: We can manage continuous integration workflows in one place.

## Consequences
- Requires careful management of CI pipelines to only run necessary jobs.
- Clear directory separation is required (e.g., `api/`, `web/`, `infra/`).
