"""
Register MCP (Model Context Protocol) tools for agents to use.
"""
from mcp.server.fastmcp import FastMCP  # type: ignore

# Initialize a FastMCP server instance for Trail Angel
mcp = FastMCP(name="trail_angel")  # type: ignore

def register_mcp_tools():
    """
    Register all necessary MCP tools for use by agents.
    """
    # Register placeholder MCP tools
    @mcp.tool(name="plan_route")
    async def plan_route(origin: str, destination: str, days: int) -> dict:
        """Test stub for route planning tool"""
        return {"route": [origin, "...waypoint...", destination], "days": days}

    @mcp.tool(name="suggest_gear")
    async def suggest_gear(origin: str, destination: str, days: int) -> dict:
        """Test stub for gear suggestion tool"""
        return {"gear_list": ["Tent", "Sleeping Bag", "Stove"]}

    @mcp.tool(name="forecast_weather")
    async def forecast_weather(origin: str, destination: str, days: int) -> dict:
        """Test stub for weather forecast tool"""
        return {"forecast": [{"day": i+1, "weather": "Sunny"} for i in range(days)]}

    @mcp.tool(name="check_permits")
    async def check_permits(origin: str, destination: str, days: int) -> dict:
        """Test stub for permit checking tool"""
        return {"permits": {"required": False, "details": "None needed"}}

    # Additional real tools can be registered here using @mcp.tool
    pass
