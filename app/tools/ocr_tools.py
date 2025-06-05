from PIL import Image
from io import BytesIO
import pytesseract
from crewai_tools import tool

# 👇 Pure OCR function
def extract_text(file_bytes: bytes) -> str:
    """Extract raw text from a receipt image using Tesseract OCR."""
    try:
        image = Image.open(BytesIO(file_bytes)).convert("RGB")
        text = pytesseract.image_to_string(image)
        print("📸 OCR Output:\n", text)
        return text
    except Exception as e:
        return f"OCR Error: {str(e)}"

# 👇 Tool wrapper for agent use (not used in your parsing pipeline anymore)
from crewai_tools import tool
@tool("OCRTool")
def extract_text_from_receipt(file_bytes: bytes) -> str:
    """Wrapped tool for CrewAI agent."""
    return extract_text(file_bytes)

def get_ocr_tool():
    return extract_text_from_receipt