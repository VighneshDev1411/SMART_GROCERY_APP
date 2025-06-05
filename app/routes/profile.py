from fastapi import APIRouter, Depends
from app.models.user_profile import UserProfile
from app.db.user_profile import save_user_profile, get_user_profile
from app.routes.auth import get_current_user

router = APIRouter(prefix="/profile", tags=["User Profile"])

@router.post("/", response_model=UserProfile)
def save_profile(profile: UserProfile, user=Depends(get_current_user)):
    profile.user_id = user["user_id"]
    save_user_profile(profile.dict())
    return profile

@router.get("/", response_model=UserProfile)
def fetch_profile(user=Depends(get_current_user)):
    doc = get_user_profile(user["user_id"])
    return UserProfile(**doc)
