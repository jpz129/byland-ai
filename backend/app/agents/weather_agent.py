"""
WeatherAgent: fetches weather forecasts for the trip.
"""

import httpx

class WeatherAgent:
    def __init__(self, memory):
        self.memory = memory

    async def forecast(self, origin: str, destination: str, days: int) -> dict:
        """
        Fetch a simple weather forecast (stubbed).
        """
        # Placeholder: return dummy forecast
        forecast = [{"day": i, "weather": "Sunny"} for i in range(1, days+1)]
        return {"forecast": forecast}
