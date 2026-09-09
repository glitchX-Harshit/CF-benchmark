# System Architecture

## Overview
CF Benchmark is designed as a modern, decoupled monorepo application.

```mermaid
flowchart TD
    Client[Web Client - Next.js] --> API[API Server - FastAPI]
    API --> DB[(PostgreSQL)]
    API --> Redis[(Redis Cache/Queue)]
    API --> Evaluator[Evaluation Engine]
    Evaluator --> LLM[External LLM APIs]
```

## Components
1. **Frontend**: Next.js application for users to view benchmark runs and configure scenarios.
2. **Backend API**: Python FastAPI providing RESTful endpoints.
3. **Database**: PostgreSQL for storing scenarios, rubrics, runs, and results.
4. **Task Queue**: Redis-backed queue for asynchronous evaluation processing.
