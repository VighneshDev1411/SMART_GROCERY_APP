from fastapi import APIRouter, Depends
from app.db.alerts import get_user_alerts
from app.routes.auth import get_current_user

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("/")
def fetch_alerts(user=Depends(get_current_user)):
    user_id = user["user_id"]
    alerts = get_user_alerts(user_id)
    return alerts
