"""
PermitsAgent: checks permit requirements for the trip.
"""

class PermitsAgent:
    def __init__(self, memory):
        self.memory = memory

    async def check(self, origin: str, destination: str, days: int) -> dict:
        """
        Return permit info (stubbed).
        """
        # Placeholder permit requirements
        permits = {"required": False, "details": "No permits needed for this route"}
        return {"permits": permits}
