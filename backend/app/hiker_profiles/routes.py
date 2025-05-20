from fastapi import APIRouter, HTTPException, Depends
from typing import Any
from uuid import uuid4

from sqlalchemy.orm import Session

from app.hiker_profiles.schemas import UserProfile, ProfileUpdate
from app.hiker_profiles.db import SessionLocal
from app.hiker_profiles import models

router = APIRouter(prefix="/hiker_profiles", tags=["hiker_profiles"])

# In-memory store for demo purposes
_profiles_store: dict[str, UserProfile] = {}

# Add dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/start", response_model=UserProfile)
async def start_profile_chat(user_id: str, db: Session = Depends(get_db)) -> Any:
    """
    Initialize a new hiker profile and start conversational onboarding.
    """
    db_user = models.User(user_id=user_id)
    db.add(db_user)
    db_profile = models.UserProfile(
        user_id=user_id,
        hiking_experience="",
        gear_style="",
        preferred_terrain=[],
        personality_tags=[],
        dietary_needs=None,
        medical_notes=None,
        profile_summary="",
        profile_complete=False,
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.post("/update/{user_id}", response_model=UserProfile)
async def update_profile(user_id: str, data: ProfileUpdate) -> Any:
    """
    Update structured fields and summary for an existing profile.
    """
    if user_id not in _profiles_store:
        raise HTTPException(status_code=404, detail="Profile not found")
    profile = _profiles_store[user_id]
    update_data = data.dict(exclude_none=True)
    for key, value in update_data.items():
        setattr(profile, key, value)
    # Placeholder: update summary if provided
    _profiles_store[user_id] = profile
    return profile

@router.get("/{user_id}", response_model=UserProfile)
async def get_profile(user_id: str) -> Any:
    """
    Fetch the full user profile.
    """
    profile = _profiles_store.get(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.post("/edit/{user_id}", response_model=UserProfile)
async def edit_profile(user_id: str, data: ProfileUpdate) -> Any:
    """
    Manually edit existing profile fields.
    """
    return await update_profile(user_id, data)
