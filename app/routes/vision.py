from fastapi import APIRouter, UploadFile, File
from app.services.vision_detector import detect_items_from_image
from app.models.vision_response import VisionResponse, DetectedItem
from app.services.vision_postprocess import postprocess_vision_output
from app.models.inventory_item import EnrichedInventoryResponse, EnrichedItem
router = APIRouter(prefix="/vision", tags=["Vision"])

@router.post('/scan-fridge', response_model=EnrichedInventoryResponse)
async def scan_fridge(file: UploadFile = File(...)):
    image_bytes = await file.read()
    raw_detections = detect_items_from_image(image_bytes)
    enriched = postprocess_vision_output(raw_detections)
    # detected = detect_items_from_image(image_bytes)
    return EnrichedInventoryResponse(
        items_detected=[EnrichedItem(**item) for item in enriched]
    )

#**item imp concept python3