from apscheduler.schedulers.background import BackgroundScheduler
from app.services.notifier import create_notification
from app.memory.receipt_memory import get_all_receipts
from app.db.user_profile import get_user_budget
from app.db.fridge import get_fridge_items
from datetime import datetime, timedelta

scheduler = BackgroundScheduler()

def check_budget_job():
    user_id = "user_123"
    receipts = get_all_receipts(user_id)
    total_spent = sum(item["price"] for r in receipts for item in r["items"])
    budget = get_user_budget(user_id)

    if total_spent > budget:
        create_notification(
            user_id=user_id,
            message=f"You've spent {total_spent}, over your {budget} weekly budget!",
            type_="budget"
        )

def check_expiry_job():
    user_id = "user_123"  # will be dynamic later
    items = get_fridge_items(user_id)
    soon = []

    for item in items:
        expiry_str = item.get("expiry_date")
        if expiry_str:
            expiry = datetime.strptime(expiry_str, "%Y-%m-%d")
            if 0 <= (expiry - datetime.utcnow()).days <= 2:
                soon.append(item["name"])

    if soon:
        msg = f"⚠️ The following items are expiring soon: {', '.join(soon)}"
        create_notification(user_id=user_id, message=msg, type_="expiry")

def start_scheduler():
    print("🕒 Scheduler started")
    scheduler.add_job(check_budget_job, trigger="interval", days=1)
    scheduler.start()
    # Run once immediately for debugging
    check_budget_job()
    check_expiry_job()
