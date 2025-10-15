from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.db import Base, engine, SessionLocal
from app.scheduler import start_scheduler
from app.models import Conso

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Demo API Conso Électrique")

@app.on_event("startup")
def startup_event():
    start_scheduler()

@app.get("/")
def root():
    return {"message": "API de démo opérationnelle"}

@app.get("/data")
def get_data():
    """Récupère toutes les mesures stockées."""
    db: Session = SessionLocal()
    rows = db.query(Conso).order_by(Conso.timestamp.desc()).limit(20).all()
    db.close()
    return [{"timestamp": r.timestamp, "value": r.value} for r in rows]


