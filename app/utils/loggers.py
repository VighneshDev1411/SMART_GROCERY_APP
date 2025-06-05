import datetime

def log_event(event_type: str, content:str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{event_type.upper()}] {content}")