from crewai_tools import tool
from sentence_transformers import SentenceTransformer
import chromadb
import json

# Initialize model and ChromaDB
model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("recipes")

# Load recipes (same as before)
def load_recipes_to_chroma():
    with open("app/data/recipes.json") as f:
        data = json.load(f)
    for i, recipe in enumerate(data):
        text = recipe["title"] + " " + " ".join(recipe["ingredients"])
        embedding = model.encode(text).tolist()
        collection.add(
            documents=[json.dumps(recipe)],
            embeddings=[embedding],
            ids=[f"recipe_{i}"]
        )
    print("✅ Recipes embedded.")

# Define a custom vector search tool
@tool("Recipe Search Tool")
def recipe_search_tool(query: str) -> str:
    """Search for recipes based on ingredients using vector similarity."""
    results = collection.query(
        query_embeddings=[model.encode(query).tolist()],
        n_results=3
    )
    return str(results["documents"])  # Return matching recipes