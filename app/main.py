from fastapi import FastAPI
from app.scheduler import start_scheduler
from app.db import Base, engine

app = FastAPI(title="API Conso Elec")

# Création des tables au démarrage
Base.metadata.create_all(bind=engine)

# Lancer le scheduler au démarrage
scheduler = start_scheduler()

@app.get("/")
def root():
    return {"message": "API conso en ligne, scheduler actif"}
