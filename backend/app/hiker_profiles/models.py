from sqlalchemy import Column, String, Boolean, ARRAY, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .db import Base

class User(Base):
    __tablename__ = 'users'
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)

class UserProfile(Base):
    __tablename__ = 'user_profiles'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), index=True)
    hiking_experience = Column(Text)
    gear_style = Column(Text)
    preferred_terrain = Column(ARRAY(Text))
    personality_tags = Column(ARRAY(Text))
    dietary_needs = Column(Text, nullable=True)
    medical_notes = Column(Text, nullable=True)
    profile_summary = Column(Text)
    profile_complete = Column(Boolean, default=False)
