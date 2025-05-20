from fastapi import FastAPI
from dotenv import load_dotenv  # type: ignore
import os

from app.hiker_profiles.routes import router as hiker_profiles_router

# Load environment variables
default_env = os.getenv("APP_ENV", None)
load_dotenv()

# Initialize FastAPI app
title = "ByLand.ai API"
app = FastAPI(title=title)

# Include only the hiker profiles router
app.include_router(hiker_profiles_router)
