from fastapi import APIRouter
from app.models.cart import SmartCartRequest, SmartCartResponse, GroceryItem
from app.agents.smart_cart_agent import build_cart_prompt, run_smart_cart_task

router = APIRouter(prefix="/cart", tags=["SmartCart"])

@router.post("/generate", response_model=SmartCartResponse)
async def generate_cart(request: SmartCartRequest):
    prompt = build_cart_prompt(request.preferences, request.past_items)
    # raw_output = run_smart_cart_task(prompt).output
    raw_output = str(run_smart_cart_task(prompt))


    items = []
    for line in raw_output.strip().split("\n"):
        if "|" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4:
                try:
                    items.append(GroceryItem(
                        name=parts[0],
                        category=parts[1],
                        price=float(parts[2].replace("₹", "").strip()),
                        quantity=parts[3]
                    ))
                except:
                    continue
    return SmartCartResponse(suggested_items=items)
