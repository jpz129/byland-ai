from langgraph.graph.graph import Graph
from langchain_community.chat_models import ChatOpenAI  # type: ignore
from mcp.client.streamable_http import streamablehttp_client  # type: ignore
from mcp.client.streamable_http import streamablehttp_client  # type: ignore  # ensure module visibility after extras install
from mcp import ClientSession  # type: ignore

from app.memory import get_memory


def build_trip_planner_graph(memory) -> Graph:
    """
    Build a LangGraph workflow for planning a backpacking trip.
    """
    graph = Graph(name="trip_planner")
    # bind an LLM instance for graph execution
    graph.set_llm(ChatOpenAI(temperature=0))

    @graph.node(name="route")
    async def route_node(origin: str, destination: str, days: int):
        # Call MCP tool for route planning
        async with streamablehttp_client("http://localhost:8000/mcp") as (r, w, _):
            async with ClientSession(r, w) as session:
                await session.initialize()
                return await session.call_tool(
                    "plan_route", {"origin": origin, "destination": destination, "days": days}
                )

    @graph.node(name="gear")
    async def gear_node(origin: str, destination: str, days: int):
        # Call MCP tool for gear suggestions
        async with streamablehttp_client("http://localhost:8000/mcp") as (r, w, _):
            async with ClientSession(r, w) as session:
                await session.initialize()
                return await session.call_tool(
                    "suggest_gear", {"origin": origin, "destination": destination, "days": days}
                )

    @graph.node(name="weather")
    async def weather_node(origin: str, destination: str, days: int):
        # Call MCP tool for weather forecast
        async with streamablehttp_client("http://localhost:8000/mcp") as (r, w, _):
            async with ClientSession(r, w) as session:
                await session.initialize()
                return await session.call_tool(
                    "forecast_weather", {"origin": origin, "destination": destination, "days": days}
                )

    @graph.node(name="permits")
    async def permits_node(origin: str, destination: str, days: int):
        # Call MCP tool for permit checking
        async with streamablehttp_client("http://localhost:8000/mcp") as (r, w, _):
            async with ClientSession(r, w) as session:
                await session.initialize()
                return await session.call_tool(
                    "check_permits", {"origin": origin, "destination": destination, "days": days}
                )

    return graph

async def run_trip_planner(origin: str, destination: str, days: int):
    """
    Execute the trip planner graph and return combined outputs.
    """
    memory = get_memory()
    graph = build_trip_planner_graph(memory)
    result = await graph.run({"origin": origin, "destination": destination, "days": days})
    # result is a dict with keys 'route', 'gear', 'weather', 'permits'
    return {
        "route": result.get("route").get("route"),
        "gear_list": result.get("gear").get("gear_list"),
        "forecast": result.get("weather").get("forecast"),
        "permits": result.get("permits").get("permits")
    }
