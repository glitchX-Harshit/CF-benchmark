# ClozFlow

ClozFlow is a sales intelligence platform focused on understanding sales conversations, evaluating seller responses, and analyzing objection handling through the **CF Benchmark** system.

## Architecture

This is a Python-first architecture.

```text
Frontend
    React + Vite + Tailwind V4

Backend
    Python + FastAPI

Intelligence
    Python + CF Engine

Database
    PostgreSQL

Infrastructure
    Docker + Redis
```

## Local Setup

### Prerequisites
- Node.js >= 18
- pnpm
- Python >= 3.10
- Docker Desktop

### 1. Environment
Copy `.env.example` to `.env` in the root.

### 2. Infrastructure
Start the database and redis:
```bash
docker-compose up -d
```

### 3. Backend (FastAPI & CF Engine)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e cf_engine
pip install -e backend

cd backend
uvicorn app.main:app --reload --port 8000
```

### 4. Frontend
```powershell
cd frontend
npm install
npm run dev
```

The frontend will run on `http://localhost:5173`.
