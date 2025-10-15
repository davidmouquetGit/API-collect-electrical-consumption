from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from app.api_client import get_data
from app.db import SessionLocal
from app.models import Conso
from sqlalchemy.dialects.postgresql import insert

def fetch_and_store():
    print(f"[{datetime.now()}] Récupération des données...")
    data = get_data()
    db = SessionLocal()
    try:
        for record in data["measurements"]:
            stmt = insert(Conso).values(
                timestamp=record["timestamp"],
                value=record["value"]
            ).on_conflict_do_nothing(index_elements=['timestamp'])
            db.execute(stmt)
        db.commit()
        print("Données enregistrées (sans doublons).")
    except Exception as e:
        db.rollback()
        print(f"Erreur : {e}")
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_store, "interval", minutes=30)
    scheduler.start()
    print("Scheduler lancé (toutes les 30 min).")
    return scheduler
