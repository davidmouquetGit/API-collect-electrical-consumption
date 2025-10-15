from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from app.simulateur import generate_fake_data
from app.db import SessionLocal
from app.crud import insert_data

def collect_fake_data():
    db = SessionLocal()
    try:
        data = generate_fake_data()
        insert_data(db, data)
        print(f"[{datetime.now()}] → {data[0]}")
    except Exception as e:
        print("Erreur :", e)
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(collect_fake_data, "interval", seconds=30)
    scheduler.start()
    print("Scheduler lancé (toutes les 30 s)")
