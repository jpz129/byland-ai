# LangGraph state machine for hiker profile onboarding
# This is a scaffold for the conversational onboarding flow using LangGraph and LangChain

from typing import Dict, Any, Callable

# Placeholder for LangGraph and LangChain imports
# from langgraph import StateMachine, Node, Transition
# from langchain.output_parsers import OutputParser

# Define the states for the onboarding flow
STATES = [
    "intro",
    "experience",
    "gear",
    "terrain",
    "personality",
    "safety",
    "summary",
    "confirmation",
]

# State handler registry
default_handlers: Dict[str, Callable[[Dict[str, Any], str], Dict[str, Any]]] = {}

def handle_intro(state: Dict[str, Any], user_input: str) -> Dict[str, Any]:
    state["current_state"] = "experience"
    state["messages"] = state.get("messages", []) + [
        {"role": "system", "content": "Welcome to ByLand.ai! Let's build your hiker profile. First, tell me about your hiking experience."}
    ]
    return state

def handle_experience(state: Dict[str, Any], user_input: str) -> Dict[str, Any]:
    state["hiking_experience"] = user_input
    state["current_state"] = "gear"
    state["messages"] = state.get("messages", []) + [
        {"role": "system", "content": "Great! What is your preferred gear style? (e.g., ultralight, luxury, hammock, tent, cowboy camping)"}
    ]
    return state

def handle_gear(state: Dict[str, Any], user_input: str) -> Dict[str, Any]:
    state["gear_style"] = user_input
    state["current_state"] = "terrain"
    state["messages"] = state.get("messages", []) + [
        {"role": "system", "content": "What terrain do you prefer? (desert, alpine, coastal, forest, etc.)"}
    ]
    return state

def handle_terrain(state: Dict[str, Any], user_input: str) -> Dict[str, Any]:
    state["preferred_terrain"] = [t.strip() for t in user_input.split(",")]
    state["current_state"] = "personality"
    state["messages"] = state.get("messages", []) + [
        {"role": "system", "content": "How would you describe your trail personality? (introverted, adventurous, social, poetic, etc.)"}
    ]
    return state

def handle_personality(state: Dict[str, Any], user_input: str) -> Dict[str, Any]:
    state["personality_tags"] = [p.strip() for p in user_input.split(",")]
    state["current_state"] = "safety"
    state["messages"] = state.get("messages", []) + [
        {"role": "system", "content": "Any dietary needs, allergies, or medical notes you'd like to share?"}
    ]
    return state

def handle_safety(state: Dict[str, Any], user_input: str) -> Dict[str, Any]:
    state["dietary_needs"] = user_input
    state["current_state"] = "summary"
    state["messages"] = state.get("messages", []) + [
        {"role": "system", "content": "Thanks! Generating your hiker profile summary..."}
    ]
    return state

def handle_summary(state: Dict[str, Any], user_input: str) -> Dict[str, Any]:
    # Placeholder: In production, use LLM to generate summary
    summary = f"{state.get('hiking_experience', '')}, {state.get('gear_style', '')}, {', '.join(state.get('preferred_terrain', []))}, {', '.join(state.get('personality_tags', []))}, {state.get('dietary_needs', '')}"
    state["profile_summary"] = summary
    state["current_state"] = "confirmation"
    state["messages"] = state.get("messages", []) + [
        {"role": "system", "content": f"Here is your profile summary: {summary}. Would you like to confirm or edit?"}
    ]
    return state

def handle_confirmation(state: Dict[str, Any], user_input: str) -> Dict[str, Any]:
    if user_input.lower() in ["yes", "confirm", "ok", "looks good"]:
        state["profile_complete"] = True
        state["messages"] = state.get("messages", []) + [
            {"role": "system", "content": "Profile complete!"}
        ]
    else:
        state["profile_complete"] = False
        state["messages"] = state.get("messages", []) + [
            {"role": "system", "content": "Let's edit your profile. Which part would you like to change?"}
        ]
    return state

default_handlers = {
    "intro": handle_intro,
    "experience": handle_experience,
    "gear": handle_gear,
    "terrain": handle_terrain,
    "personality": handle_personality,
    "safety": handle_safety,
    "summary": handle_summary,
    "confirmation": handle_confirmation,
}

def run_onboarding_state(state: Dict[str, Any], user_input: str) -> Dict[str, Any]:
    current = state.get("current_state", "intro")
    handler = default_handlers.get(current, lambda s, u: s)
    return handler(state, user_input)
