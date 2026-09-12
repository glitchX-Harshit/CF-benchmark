from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.router import api_router
from .core.config import settings
from .core.database import Base, engine
# Import models to ensure they are registered with Base
from .models.scenario import Scenario

# Create tables for MVP
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ClozFlow API",
    version="0.1.0",
    description="ClozFlow core API including CF Benchmark evaluation",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"], # TODO: restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to ClozFlow API"}
