from crewai import Crew, Task
from app.agents.base_agent import create_base_agent
from app.tools.recipe_search_tool import recipe_search_tool
# from app.memory.memory_store import recipe_memory  # Optional

# 1. Agent A: Pantry Interpreter
def pantry_agent():
    return create_base_agent(
        name="PantryInterpreter",
        goal="Understand the user's pantry and narrow down possible dish types",
        backstory="You're great at analyzing available ingredients and estimating what can be cooked.",
    )

# 2. Agent B: Recipe Suggester (uses tool)
def recipe_agent():
    return create_base_agent(
        name="RecipeSuggester",
        goal="Find the best recipe using available ingredients",
        backstory="You are a recipe expert with access to a recipe database.",
        tools=[recipe_search_tool] 
    )

# Multi-agent orchestrator
def run_recipe_crew(pantry: list[str]) -> dict:
    pantry_str = ", ".join(pantry)

    a = pantry_agent()
    b = recipe_agent()

    task1 = Task(
        description=f"Given the pantry: [{pantry_str}], determine what categories of recipes are possible.",
        agent=a,
        expected_output="Recipe category and ingredient matches"
    )

    task2 = Task(
        description=f"Use these pantry items: [{pantry_str}]. Search for a recipe and present it with title, ingredients, and steps.",
        agent=b,
        expected_output="Full recipe with steps"
    )

    crew = Crew(
        agents=[a, b],
        tasks=[task1, task2],
        # memory=recipe_memory,
        verbose=True
    )

    result = crew.kickoff(return_all_outputs=True)
    return {
        "reasoning": result[0],
        "recipe": result[1]
    }