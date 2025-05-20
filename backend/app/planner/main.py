from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from dotenv import load_dotenv  # type: ignore
import os
load_dotenv()

from app.planner.tools.mcp_tools import register_mcp_tools, mcp
from app.planner.pipelines.trip_planner_graph import run_trip_planner

# Initialize FastAPI app
app = FastAPI(title="Trail Angel Planner")

# Register MCP tools and mount the MCP HTTP app
register_mcp_tools()
app.mount("/mcp", mcp.streamable_http_app())

# Pydantic model for trip request
template = BaseModel
class TripRequest(template):
    origin: str
    destination: str
    days: int

@app.post("/plan")
async def plan_trip(request: TripRequest):
    """
    Main endpoint to plan a backpacking trip
    """
    # Log incoming request
    print(f"[plan_trip] Received: origin={request.origin}, destination={request.destination}, days={request.days}")
    try:
        # Execute the trip planner graph workflow
        result = await run_trip_planner(request.origin, request.destination, request.days)
        # Log result before returning
        print(f"[plan_trip] Result: {result}")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents")
async def list_agents():
    """
    List available agents and their purpose
    """
    return {
        "agents": [
            "route_planner", "gear_agent", "weather_agent", "permits_agent"
        ]
    }
