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

# TODO: Move OnboardingSession to models.py for consistency with other models
# TODO: Add Alembic or similar for DB migrations
class OnboardingSession(models.Base):
    __tablename__ = "onboarding_sessions"
    user_id = Column(String, primary_key=True)
    state = Column(JSON, nullable=False)

# TODO: Validate and sanitize user_id input more robustly (utility function, regex, error handling)
# TODO: Add logging for all endpoints (use logging module, log requests, responses, errors)
# TODO: Add error handling for DB connection issues (try/except, return 503 or 500)
# TODO: Add authentication/authorization for user endpoints (OAuth2, API keys, etc.)
# TODO: Add OpenAPI docstrings for all endpoints (summary, description, request/response examples)
# TODO: Add tests for all endpoints (unit, integration, edge cases)
# TODO: Refactor duplicate UUID parsing logic into a utility function (DRY)
# TODO: Integrate LangGraph official checkpointer API for advanced features (versioning, replay)
# TODO: Add endpoint to reset onboarding session (clear state, restart onboarding)
# TODO: Add endpoint to delete user/profile (GDPR compliance, user control)
# TODO: Add pagination for user/profile listing if needed (for admin or analytics)
# TODO: Remove legacy planner code if not needed (clean up planner/)
# TODO: Add endpoint to list all user profiles (admin, analytics)
# TODO: Add endpoint to export user profile data (user request, GDPR)
# TODO: Add endpoint to import user profile data (user migration)
# TODO: Add endpoint to get onboarding session state (debugging, admin)
# TODO: Add endpoint to list all onboarding sessions (admin, analytics)
# TODO: Add endpoint to update onboarding session state (admin, debugging)
# TODO: Add endpoint to get API/server health (readiness/liveness probe)
# TODO: Add endpoint to get API version/build info (debugging, support)

@router.post("/start", response_model=UserProfile)
async def start_profile_chat(user_id: str, db: Session = Depends(get_db)) -> Any:
    """
    Initialize a new hiker profile and start conversational onboarding.
    """
    # TODO: Refactor to use utility for UUID parsing
    # TODO: Add check for valid user_id format (regex, error handling)
    # TODO: Add logging for profile creation (info, warning, error)
    # TODO: Add error handling for DB commit/refresh failures
    import uuid
    # Ensure user_id is a valid UUID (strip quotes if present)
    if user_id.startswith('"') or user_id.startswith("'"):
        user_id = user_id.strip('"').strip("'")
    user_id_obj = uuid.UUID(user_id)
    # Check if user already exists
    db_user = db.query(models.User).filter(models.User.user_id == user_id_obj).first()
    if not db_user:
        db_user = models.User(user_id=user_id_obj)
        db.add(db_user)
    # Check if profile already exists
    db_profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id_obj).first()
    if not db_profile:
        db_profile = models.UserProfile(
            user_id=str(user_id_obj),  # Ensure this is a string for Pydantic
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
    # Convert user_id to string for response
    db_profile.user_id = str(db_profile.user_id)
    return db_profile

@router.post("/update/{user_id}", response_model=UserProfile)
async def update_profile(user_id: str, data: ProfileUpdate, db: Session = Depends(get_db)) -> Any:
    # TODO: Refactor to use utility for UUID parsing
    # TODO: Add logging for profile update (info, warning, error)
    # TODO: Add validation for update fields (type, allowed values)
    # TODO: Add error handling for DB commit/refresh failures
    import uuid
    # Ensure user_id is a valid UUID
    if user_id.startswith('"') or user_id.startswith("'"):
        user_id = user_id.strip('"').strip("'")
    user_id_obj = uuid.UUID(user_id)
    db_profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id_obj).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    update_data = data.dict(exclude_none=True)
    for key, value in update_data.items():
        setattr(db_profile, key, value)
    db.commit()
    db.refresh(db_profile)
    db_profile.user_id = str(db_profile.user_id)
    return db_profile

@router.get("/{user_id}", response_model=UserProfile)
async def get_profile(user_id: str, db: Session = Depends(get_db)) -> Any:
    # TODO: Refactor to use utility for UUID parsing
    # TODO: Add logging for profile retrieval (info, warning, error)
    # TODO: Add error handling for DB query failures
    import uuid
    # Ensure user_id is a valid UUID
    if user_id.startswith('"') or user_id.startswith("'"):
        user_id = user_id.strip('"').strip("'")
    user_id_obj = uuid.UUID(user_id)
    db_profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id_obj).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    db_profile.user_id = str(db_profile.user_id)
    return db_profile

@router.post("/edit/{user_id}", response_model=UserProfile)
async def edit_profile(user_id: str, data: ProfileUpdate, db: Session = Depends(get_db)) -> Any:
    """
    Manually edit existing profile fields.
    """
    # TODO: Add logging for manual profile edit (info, warning, error)
    # TODO: Add error handling for DB commit/refresh failures
    return await update_profile(user_id, data, db)

@router.post("/chat/{user_id}")
async def profile_chat(
    user_id: str,
    user_input: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    # TODO: Refactor to use utility for UUID parsing
    # TODO: Add logging for onboarding chat (info, warning, error)
    # TODO: Add error handling for state machine failures (try/except)
    # TODO: Add support for LLM/Chainlit integration (frontend, streaming)
    # TODO: Add support for onboarding session versioning/replay (LangGraph checkpointer)
    # TODO: Add error handling for DB commit/refresh failures
    import uuid
    # Ensure user_id is a valid UUID
    if user_id.startswith('"') or user_id.startswith("'"):
        user_id = user_id.strip('"').strip("'")
    user_id_obj = uuid.UUID(user_id)
    # Load state from DB (persistent, not just in-memory)
    session = db.query(OnboardingSession).filter(OnboardingSession.user_id == str(user_id_obj)).first()
    if session:
        state = session.state
    else:
        state = {"user_id": str(user_id_obj), "current_state": "intro", "messages": []}
    # Advance the state machine
    new_state = run_onboarding_state(state, user_input)
    # Persist state to DB
    if session:
        session.state = new_state
    else:
        session = OnboardingSession(user_id=str(user_id_obj), state=new_state)
        db.add(session)
    db.commit()
    # Optionally, persist to user profile if profile_complete
    if new_state.get("profile_complete"):
        db_profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id_obj).first()
        if not db_profile:
            db_profile = models.UserProfile(user_id=str(user_id_obj))
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
