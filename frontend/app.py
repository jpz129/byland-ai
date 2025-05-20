# app.py - Chainlit entrypoint for ByLand.ai
# TODO: Add logging for frontend events and errors
# TODO: Add error handling for API calls
# TODO: Add authentication support if needed
# TODO: Add admin/analytics dashboard UI (optional)
# TODO: Add profile management UI (optional)
# TODO: Add onboarding session reset and export/import features (optional)

import chainlit as cl
import os
import requests

# TODO: Load API URL from .env
API_URL = os.getenv("BYLAND_API_URL", "http://localhost:8000/hiker_profiles")

@cl.on_message
async def on_message(message: cl.Message):
    """
    Main conversational handler for onboarding flow.
    TODO: Add user_id management (login, session, etc.)
    TODO: Add error handling for backend failures
    TODO: Add loading state UI
    TODO: Add support for profile CRUD and admin features
    """
    user_id = "demo-user-uuid"  # TODO: Replace with real user/session management
    try:
        resp = requests.post(f"{API_URL}/chat/{user_id}", json={"user_input": message.content})
        resp.raise_for_status()
        data = resp.json()
        # TODO: Render messages in a more user-friendly way
        await cl.Message(content="\n".join(data.get("messages", []))).send()
    except Exception as e:
        await cl.Message(content=f"Error: {e}").send()

# TODO: Add Chainlit UI customizations (theme, branding, etc.)
# TODO: Add onboarding start/reset commands
# TODO: Add profile view/edit commands
# TODO: Add admin/analytics commands (optional)
