from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from app.routes import cart
from app.routes import recipe
# from app.routes import recipe
from app.routes import vision
from app.routes import ocr
from app.utils.scheduler import start_scheduler
load_dotenv()
from contextlib import asynccontextmanager
from app.routes import profile
from app.memory.receipt_memory import get_all_receipts
from app.routes import alerts


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield

app = FastAPI(title="Smart Grocery App", version="1.0", lifespan=lifespan)

app.include_router(cart.router)
# app.include_router(recipe.router)
app.include_router(recipe.router)
app.include_router(vision.router)
app.include_router(ocr.router)
app.include_router(profile.router)
app.include_router(alerts.router)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Smart Grocery App Backend is live"}

@app.get("/health")
async def health_check():
    return {"status": "CrewAI backend is live"}

@app.get("/debug/show-receipts")
def debug_receipts():
    return get_all_receipts("user_123")

from app.utils.scheduler import check_budget_job, check_expiry_job

@app.get("/debug/run-alerts")
async def run_alerts():
    check_budget_job()
    check_expiry_job()
    return {"status": "manual check done"}
