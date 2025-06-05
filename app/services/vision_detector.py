from ultralytics import YOLO
from PIL import Image
import torch
import io

model = YOLO("yolov8m.pt")

def detect_items_from_image(image_bytes: bytes, confidence_threshold: float = 0.5):
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        results = model.predict(image, conf=confidence_threshold)
        
        if not results:
            return []
        
        detected_items = []

        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            name = model.names[cls_id]
            conf = float(box.conf[0])
            detected_items.append({
                "name": name,
                "confidence": round(conf, 2)
            })

        return detected_items
    except Exception as e:
        print("Detection error: ", e)
        return []