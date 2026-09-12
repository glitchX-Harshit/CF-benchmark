from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.router import api_router
from .core.config import settings
from .core.database import Base, engine
# Import models to ensure they are registered with Base
from .models.scenario import Scenario
from .models.evaluation import Evaluation

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

import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Serve frontend statically if it exists (for Render / Production)
frontend_dist = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "dist")

if os.path.exists(frontend_dist):
    # Mount the assets directory directly
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
    
    # Catch-all route to serve the SPA
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Ignore /api routes
        if full_path.startswith("api/"):
            return {"error": "API route not found"}
            
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
            
        # Fallback to index.html for React Router
        return FileResponse(os.path.join(frontend_dist, "index.html"))
else:
    @app.get("/")
    def root():
        return {"message": "Welcome to ClozFlow API. Frontend build not found."}
