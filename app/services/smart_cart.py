from app.models.cart import UserPreferences, GroceryItem
from app.agents.llm_client import call_llm
from typing import List
from app.db.cart_ops import save_cart

def build_prompt(preferences: UserPreferences, past_items: List[GroceryItem]) -> str:
    past_item_names = [item.name for item in past_items]

    prompt = f"""
You are a grocery shopping assistant.
The user has the following dietary restrictions: {preferences.dietary_restrictions}
Their preferred stores are: {preferences.preferred_stores}
Their weekly grocery budget is ₹{preferences.weekly_budget}.

Their past grocery items include: {past_item_names}

Based on this, generate a new weekly grocery list that:
- Fits the budget
- Avoids restricted items
- Contains healthy and diverse choices

Output format:
Item Name | Category | Price (in ₹) | Quantity

Example:
Tomatoes | Vegetables | ₹40 | 1kg
Milk | Dairy | ₹55 | 1L
"""

    return prompt


async def generate_smart_cart(user_id, preferences: UserPreferences, past_items: List[GroceryItem]) -> List[GroceryItem]:
    
    prompt = build_prompt(preferences, past_items)
    raw_response = await call_llm(prompt)

    items = []
    for line in raw_response.strip().split("\n"):
        if "|" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4:
                try:
                    price = float(parts[2].replace("₹", "").strip())
                    items.append(GroceryItem(
                        name=parts[0],
                        category=parts[1],
                        price=price,
                        quantity=parts[3]
                    ))
                except Exception as e:
                    print("Parse error:", e)
                    continue
    save_cart(user_id, items)
    
    
    return items
