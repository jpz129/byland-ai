"""
GearAgent: suggests gear for a backpacking trip.
"""

class GearAgent:
    def __init__(self, memory):
        self.memory = memory

    async def suggest(self, origin: str, destination: str, days: int) -> dict:
        """
        Suggest a gear checklist based on trip details.
        """
        # Placeholder gear list
        gear = [
            "Tent",
            "Sleeping Bag",
            "Hiking Boots",
            "Water Filter",
            "First Aid Kit"
        ]
        return {"gear_list": gear}
