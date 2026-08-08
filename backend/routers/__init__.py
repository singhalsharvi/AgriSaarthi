from backend.routers.crop import router as crop_router
from backend.routers.disease import router as disease_router
from backend.routers.government_schemes import router as government_schemes_router

__all__ = ["government_schemes_router", "crop_router", "disease_router"]
