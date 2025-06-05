from crewai import Agent, Task, Crew
from app.agents.base_agent import create_base_agent
# from app.tools.recipe_sear÷ch_tool import get_recipe_tool
from app.tools.recipe_search_tool import recipe_search_tool

def create_recipe_agent():
    return Agent(
        role="RecipeSuggester",
        goal="Find a recipe using available pantry ingredients",
        backstory="You are a creative chef who only uses what's in the user's kitchen.",
        tools=[recipe_search_tool],
        verbose=True
    )

def run_recipe_agent(pantry: list[str]) -> str:
    query = ", ".join(pantry)
    agent = create_recipe_agent()

    task = Task(
        description=f"Using pantry items [{query}], find a recipe and format it as:\nTitle, Ingredients, Steps.",
        agent=agent,
        expected_output="A structured recipe that uses only pantry items"
    )

    crew = Crew(agents=[agent], tasks=[task])
    result = crew.kickoff()
    return result
