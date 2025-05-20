from fastapi import APIRouter, HTTPException, Depends, Body
from typing import Any
from sqlalchemy.orm import Session
from sqlalchemy import Column, String, JSON

from app.hiker_profiles.schemas import UserProfile, ProfileUpdate
from app.hiker_profiles.db import SessionLocal
from app.hiker_profiles import models
from app.hiker_profiles.graph import run_onboarding_state
import json

router = APIRouter(prefix="/hiker_profiles", tags=["hiker_profiles"])

# Add dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# In-memory session store for demo (replace with Redis or DB for production)
session_store = {}

# Add this model to store onboarding state persistently
class OnboardingSession(models.Base):
    __tablename__ = "onboarding_sessions"
    user_id = Column(String, primary_key=True)
    state = Column(JSON, nullable=False)

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
async def update_profile(user_id: str, data: ProfileUpdate, db: Session = Depends(get_db)) -> Any:
    """
    Update structured fields and summary for an existing profile.
    """
    db_profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    update_data = data.dict(exclude_none=True)
    for key, value in update_data.items():
        setattr(db_profile, key, value)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.get("/{user_id}", response_model=UserProfile)
async def get_profile(user_id: str, db: Session = Depends(get_db)) -> Any:
    """
    Fetch the full user profile.
    """
    db_profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile

@router.post("/edit/{user_id}", response_model=UserProfile)
async def edit_profile(user_id: str, data: ProfileUpdate, db: Session = Depends(get_db)) -> Any:
    """
    Manually edit existing profile fields.
    """
    return await update_profile(user_id, data, db)

@router.post("/chat/{user_id}")
async def profile_chat(
    user_id: str,
    user_input: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    """
    Advance the onboarding state machine for a user, persisting state after each step.
    """
    # Load state from DB (persistent, not just in-memory)
    session = db.query(OnboardingSession).filter(OnboardingSession.user_id == user_id).first()
    if session:
        state = session.state
    else:
        state = {"user_id": user_id, "current_state": "intro", "messages": []}
    # Advance the state machine
    new_state = run_onboarding_state(state, user_input)
    # Persist state to DB
    if session:
        session.state = new_state
    else:
        session = OnboardingSession(user_id=user_id, state=new_state)
        db.add(session)
    db.commit()
    # Optionally, persist to user profile if profile_complete
    if new_state.get("profile_complete"):
        db_profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()
        if not db_profile:
            db_profile = models.UserProfile(user_id=user_id)
            db.add(db_profile)
        db_profile.hiking_experience = new_state.get("hiking_experience", "")
        db_profile.gear_style = new_state.get("gear_style", "")
        db_profile.preferred_terrain = new_state.get("preferred_terrain", [])
        db_profile.personality_tags = new_state.get("personality_tags", [])
        db_profile.dietary_needs = new_state.get("dietary_needs")
        db_profile.medical_notes = new_state.get("medical_notes")
        db_profile.profile_summary = new_state.get("profile_summary", "")
        db_profile.profile_complete = True
        db.commit()
        db.refresh(db_profile)
    return {"state": new_state, "messages": new_state.get("messages", [])}
