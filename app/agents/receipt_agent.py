from crewai import Agent, Task, Crew
from app.tools.ocr_tools import extract_text
from typing import Optional
from app.tools.ocr_tools import get_ocr_tool
from app.memory.receipt_memory import store_receipt
import json

def create_receipt_agent() -> Agent:
    return Agent(
        role="ReceiptParser",
        goal="Extract structured data from grocery receipt OCR text",
        backstory=(
            "You are a smart receipt parser that understands how to convert raw OCR text "
            "into structured JSON with store name, date, items and total."
        ),
        tools=[],  # ⛔ No tools needed here anymore, OCR is done outside
        verbose=True,
        memory = True
    )

def create_receipt_parsing_task(ocr_text: str) -> Task:
    return Task(
        description=(
            "You are a ReceiptParser agent. You will be given raw OCR text from a grocery receipt. "
            "Your job is to extract structured purchase information from it and return it as JSON.\n\n"
            "🔽 Here is the raw OCR text:\n"
            "------------------------------\n"
            f"{ocr_text}\n"
            "------------------------------\n\n"
            "✅ Extract and return ONLY a JSON response in this format:\n"
            '{\n'
            '  "store": "<store name>",\n'
            '  "date": "<YYYY-MM-DD>",\n'
            '  "items": [ {"name": "<item name>", "price": <float>}, ... ],\n'
            '  "total": <float>\n'
            '}\n\n'
            "Do not add any explanations or extra formatting. Only return the JSON."
        ),
        expected_output="Return only valid JSON without explanation.",
        agent=create_receipt_agent(),
        input={"ocr_text": ocr_text}
    )

def run_receipt_agent(receipt_bytes: bytes, user_id: str) -> str:
    # 🔍 Step 1: Extract OCR text
    ocr_text = extract_text(receipt_bytes)
    print("\n🧾 OCR Extracted Text:\n", ocr_text)

    # 🔍 Step 2: Pass OCR text to agent for parsing
    task = create_receipt_parsing_task(ocr_text)
    crew = Crew(agents=[task.agent], tasks=[task])
    result = crew.kickoff()

    try:
        parsed = json.loads(result)
        store_receipt(user_id=user_id, receipt_data=parsed)
    except Exception as e:
        print("Failed to store in memory", e)
    return result.tasks_output[0].raw  # ✅ Use .raw safely
