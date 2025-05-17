from langgraph import Graph
from langchain.chat_models import ChatOpenAI  # type: ignore

from app.agents.route_planner import RoutePlannerAgent
from app.agents.gear_agent import GearAgent
from app.agents.weather_agent import WeatherAgent
from app.agents.permits_agent import PermitsAgent
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
        agent = RoutePlannerAgent(memory)
        result = await agent.plan(origin, destination, days)
        return result

    @graph.node(name="gear")
    async def gear_node(origin: str, destination: str, days: int):
        agent = GearAgent(memory)
        result = await agent.suggest(origin, destination, days)
        return result

    @graph.node(name="weather")
    async def weather_node(origin: str, destination: str, days: int):
        agent = WeatherAgent(memory)
        result = await agent.forecast(origin, destination, days)
        return result

    @graph.node(name="permits")
    async def permits_node(origin: str, destination: str, days: int):
        agent = PermitsAgent(memory)
        result = await agent.check(origin, destination, days)
        return result

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
