



from fastapi import FastAPI
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from app.db import Base, engine, SessionLocal
from app.scheduler import start_scheduler
import logging
import sys

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)  # important pour Docker
    ]
)

logger = logging.getLogger(__name__)



# Crée les tables
Base.metadata.create_all(bind=engine)

# Nouveau gestionnaire de cycle de vie
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Équivalent de "startup" ---
    start_scheduler()
    yield
    # --- Équivalent de "shutdown" ---
    # (tu peux y mettre du code de nettoyage si besoin)
    print("API arrêtée proprement.")

# Initialisation de l’app FastAPI avec lifespan
app = FastAPI(title="API récupération conso électrique", lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "API récupération conso électrique running"}
