from pathlib import Path
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure project root directory is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.routers.crop import router as crop_router
from backend.routers.disease import router as disease_router
from backend.routers.government_schemes import router as government_schemes_router
from backend.routers.farmer import router as farmer_router

app = FastAPI(
    title="Crop Recommendation & Agricultural AI Backend API",
    description="Unified API server providing Crop Recommendation, Disease Detection, and Government Scheme RAG capabilities.",
    version="1.0.0",
)

# CORS middleware to allow connections from web/mobile frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount domain routers
app.include_router(government_schemes_router)
app.include_router(crop_router)
app.include_router(disease_router)
app.include_router(farmer_router)


@app.get("/", tags=["Health Check"])
def read_root():
    return {
        "status": "online",
        "service": "Agricultural AI Backend API",
        "version": "1.0.0",
        "endpoints": [
            "/government-schemes/recommend",
            "/crop/recommend",
            "/disease/analyze",
            "/disease/detect",
            "/health",
            "/docs",
        ],
    }


@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
