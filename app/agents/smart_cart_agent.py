from crewai import Agent, Task, Crew
from app.agents.base_agent import create_base_agent
from app.models.cart import UserPreferences, GroceryItem
from typing import List


def build_cart_prompt(prefs: UserPreferences, past_items: List[GroceryItem]) -> str:
    item_names = [item.name for item in past_items]
    return f"""
The user has the following preferences:
- Dietary restrictions: {prefs.dietary_restrictions}
- Preferred stores: {prefs.preferred_stores}
- Weekly grocery budget: ₹{prefs.weekly_budget}
- Past grocery items: {item_names}

Generate a new grocery list for this week that:
- Respects budget and restrictions
- Is healthy and diverse
- Return the list in format: name | category | price | quantity
"""


def create_smart_cart_agent() -> Agent:
    return create_base_agent(
        name="SmartCartPlanner",
        goal="Generate a healthy, budget-conscious grocery list based on user profile",
        backstory="You are an expert grocery planning assistant. You balance health, budget, and user preferences with precision."
    )


def run_smart_cart_task(prompt: str) -> str:
    agent = create_smart_cart_agent()
    task = Task(
        description=prompt,
        agent=agent,
        expected_output="List of groceries: name | category | price | quantity"
    )
    crew = Crew(agents=[agent], tasks=[task])
    result = crew.kickoff()
    return result
