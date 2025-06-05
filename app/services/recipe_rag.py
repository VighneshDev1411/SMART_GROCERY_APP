from app.db.recipe_store import search_recipes
from app.agents.llm_client import call_llm

async def suggest_recipe(pantry: list[str]):
    # RAG

    # RETRIEVE
    retrieved = search_recipes(pantry)

    # AUGMENT
    prompt = f"Suggest a recipe from this list: {retrieved}.\nUse only ingredients in {pantry}.\nFormat: Title, Ingredients, Steps."
    
    # GENERATE
    return await call_llm(prompt) 