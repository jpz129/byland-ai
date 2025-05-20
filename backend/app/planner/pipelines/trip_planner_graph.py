from langgraph.graph.state import StateGraph
from typing_extensions import TypedDict
from typing import Any, Dict, List
from app.planner.memory import get_memory

# Define full state schema as TypedDict
class TripState(TypedDict):
    origin: str
    destination: str
    days: int
    route: List[Any]
    gear_list: List[str]
    forecast: List[Dict[str, Any]]
    permits: Dict[str, Any]


def build_trip_planner_graph(memory) -> StateGraph:
    """
    Build a LangGraph StateGraph for planning a backpacking trip with parallel nodes.
    """
    graph = StateGraph(TripState)

    async def route_node(state):
        origin = state["origin"]
        destination = state["destination"]
        # Return only the 'route' key; other keys remain in state
        return {"route": [origin, "...waypoint...", destination]}

    graph.add_node("route_node", route_node)

    async def gear_node(state):
        # Return only the 'gear_list' key
        return {"gear_list": ["Tent", "Sleeping Bag", "Stove"]}

    graph.add_node("gear_node", gear_node)

    async def weather_node(state):
        days = state["days"]
        # Return only the 'forecast' key
        return {"forecast": [{"day": i+1, "weather": "Sunny"} for i in range(days)]}

    graph.add_node("weather_node", weather_node)

    async def permits_node(state):
        # Return only the 'permits' key
        return {"permits": {"required": False, "details": "None needed"}}

    graph.add_node("permits_node", permits_node)

    # Set entry point to 'route_node', then add edges to other nodes for parallel execution
    graph.set_entry_point("route_node")
    graph.add_edge("route_node", "gear_node")
    graph.add_edge("route_node", "weather_node")
    graph.add_edge("route_node", "permits_node")
    return graph


async def run_trip_planner(origin: str, destination: str, days: int):
    memory = get_memory()
    graph = build_trip_planner_graph(memory)
    runnable = graph.compile()
    # The input dict is passed to all nodes
    result = await runnable.ainvoke({"origin": origin, "destination": destination, "days": days})
    return {
        "route": result.get("route"),
        "gear_list": result.get("gear_list"),
        "forecast": result.get("forecast"),
        "permits": result.get("permits")
    }
