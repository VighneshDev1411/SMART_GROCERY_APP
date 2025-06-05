from fastapi import APIRouter, UploadFile, File
from app.agents.receipt_agent import run_receipt_agent
from app.models.receipt import ReceiptResponse, ReceiptItem
from fastapi.responses import JSONResponse
import json
from fastapi import Depends
from app.routes.auth import get_current_user
from app.memory.receipt_memory import store_receipt

router = APIRouter(prefix="/ocr", tags=["Receipt OCR"])

@router.post("/upload-receipt", response_model=ReceiptResponse)
async def upload_receipt(file: UploadFile = File(...), user:dict = Depends(get_current_user)):
    file_bytes = await file.read()

    agent_output = run_receipt_agent(file_bytes, user_id=user["user_id"])
    print("🤖 Agent Raw Output:", agent_output)

    try:
        parsed = json.loads(agent_output)
        print(f"📥 Storing receipt for user: {user['user_id']}")

        store_receipt(user_id=user["user_id"], receipt_data=parsed)

        return ReceiptResponse(
            store=parsed["store"],
            date=parsed["date"],
            total=parsed["total"],
            items=[ReceiptItem(**item) for item in parsed["items"]]
        )
    except Exception as e:
        return JSONResponse(
            status_code=422,
            content={
                "error": "Failed to parse receipt",
                "details": str(e),
                "raw_output": agent_output
            }
        )
