from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.services.db_service import db_service

router = APIRouter(prefix="/farmer", tags=["Farmer Profile & Activity logs"])


class FarmerProfileRequest(BaseModel):
    farmer_id: str = Field(..., example="ramesh.farmer@agrisaarthi.in")
    name: str = Field("Farmer", example="Ramesh Kumar")
    location: Optional[str] = Field(None, example="Meerut, Uttar Pradesh")
    contact_info: Optional[str] = Field(None, example="ramesh.farmer@agrisaarthi.in")
    preferred_language: Optional[str] = Field("en", example="hi")
    land_size: Optional[str] = Field(None, example="2.5 Acres")
    soil_type: Optional[str] = Field(None, example="Alluvial Soil")


class FarmerProfileResponse(BaseModel):
    status: str
    profile: Dict[str, Any]


class FarmerActivitiesResponse(BaseModel):
    status: str
    farmer_id: str
    activities: List[Dict[str, Any]]


@router.post("/profile", response_model=FarmerProfileResponse)
def upsert_profile(request: FarmerProfileRequest) -> FarmerProfileResponse:
    """Create or update a farmer profile in the SQLite database."""
    try:
        profile_dict = request.model_dump()
        farmer_id = profile_dict.pop("farmer_id")
        
        updated_profile = db_service.upsert_farmer_profile(farmer_id, profile_dict)
        return FarmerProfileResponse(status="success", profile=updated_profile)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to save farmer profile: {str(exc)}")


@router.get("/profile/{farmer_id}", response_model=FarmerProfileResponse)
def get_profile(farmer_id: str) -> FarmerProfileResponse:
    """Retrieve a farmer profile by ID. If not found, returns a default template."""
    try:
        profile = db_service.get_farmer_profile(farmer_id)
        if not profile:
            # Return a default template instead of throwing 404 to support seamless frontend sign-in
            profile = db_service.upsert_farmer_profile(farmer_id, {
                "name": "Ramesh Kumar",
                "location": "Meerut, Uttar Pradesh",
                "emailOrPhone": farmer_id
            })
            
        return FarmerProfileResponse(status="success", profile=profile)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve profile: {str(exc)}")


@router.get("/activities/{farmer_id}", response_model=FarmerActivitiesResponse)
def get_activities(farmer_id: str, limit: int = 10) -> FarmerActivitiesResponse:
    """Retrieve a farmer's recent activities (crop recommendations, disease checks, etc.)."""
    try:
        activities = db_service.get_activities(farmer_id, limit=limit)
        return FarmerActivitiesResponse(
            status="success", 
            farmer_id=farmer_id, 
            activities=activities
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve activities: {str(exc)}")
