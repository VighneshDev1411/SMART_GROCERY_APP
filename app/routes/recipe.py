from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.recipe_agent import run_recipe_agent

router = APIRouter(prefix="/recipe", tags=["Recipe"])

class RecipeRequest(BaseModel):
    pantry: list[str]

# @router.post("/suggest")
# async def suggest_recipe(request: RecipeRequest):
#     recipe = run_recipe_agent(request.pantry)
#     return {"recipe": recipe}


from app.agents.orchestrator import run_recipe_crew

@router.post("/suggest")
async def suggest_recipe(request: RecipeRequest):
    result = run_recipe_crew(request.pantry)
    return result
