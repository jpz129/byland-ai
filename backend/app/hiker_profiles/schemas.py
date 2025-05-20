from pydantic import BaseModel
from typing import List, Optional


class UserProfile(BaseModel):
    user_id: str
    hiking_experience: str
    gear_style: str
    preferred_terrain: List[str]
    personality_tags: List[str]
    dietary_needs: Optional[str] = None
    medical_notes: Optional[str] = None
    profile_summary: str = ""
    profile_complete: bool = False


class ProfileUpdate(BaseModel):
    hiking_experience: Optional[str]
    gear_style: Optional[str]
    preferred_terrain: Optional[List[str]]
    personality_tags: Optional[List[str]]
    dietary_needs: Optional[str]
    medical_notes: Optional[str]
