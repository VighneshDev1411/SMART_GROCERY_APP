from chromadb import Client
import json
from sentence_transformers import SentenceTransformer

chroma = Client()
collection = chroma.get_or_create_collection(name="recipes")
model = SentenceTransformer("all-MiniLM-L6-v2")

# def load_and_embed():
#     with open("app/data/recipes.json") as f:
#         recipes = json.load(f)
#     for recipe in recipes:
#         text = recipe["title"] + " " + " ".join(recipe["ingredients"])
#         embedding = model.encode(text).tolist()
#         collection.add(
#             documents=[json.dumps(recipe)],
#             embeddings=[embedding],
#             ids=[recipe["title"]]
#         )

def load_and_embed():
    with open("app/data/recipes.json") as f:
        recipes = json.load(f)

    print(f"Loading {len(recipes)} recipes into ChromaDB...")
    for recipe in recipes:
        text = recipe["title"] + " " + " ".join(recipe["ingredients"])
        embedding = model.encode(text).tolist()
        collection.add(
            documents=[json.dumps(recipe)],
            embeddings=[embedding],
            ids=[recipe["title"]]
        )

    print("Recipes successfully loaded!")
    print("Total in collection now:", collection.count())


# def search_recipes(pantry_items: list[str], top_k=3):
#     query = " ".join(pantry_items)
#     query_embedding = model.encode(query).tolist()
#     results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
#     return [json.loads(doc) for doc in results["documents"][0]]

def search_recipes(pantry_items: list[str], top_k=3):
    query = " ".join(pantry_items)
    query_embedding = model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    # If no documents returned
    if not results or not results.get("documents") or not results["documents"][0]:
        return []

    return [json.loads(doc) for doc in results["documents"][0]]


if __name__ == "__main__":
    load_and_embed()
    results = search_recipes(["toor dal", "spinach", "onion", "tomato", "mustard seeds", "garlic"])
    print("Search Results", results)