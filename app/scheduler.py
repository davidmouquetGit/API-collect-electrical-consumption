
from apscheduler.schedulers.background import BackgroundScheduler


from app.db import SessionLocal
from app.crud import insert_data_conso_horaire, insert_data_conso_jour
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def start_scheduler():
    logger.info("Début scheduler")
    scheduler = BackgroundScheduler()
    scheduler.add_job(collect_consohoraire_data, "interval", hours=24)
    scheduler.start()
    print("Scheduler lancé (toutes les 24 h)")


def collect_consohoraire_data():
    logger.info("Début collect data conso horaire")
    db = SessionLocal()
    try:
        data = get_data_horaire_from_api()
        data = data["interval_reading"]
        insert_data_conso_horaire(db, data)
        insert_data_conso_jour(db, data)
        
    except Exception as e:
        print("Erreur :", e)
    finally:
        logger.info("collect data conso horaire bien déroulée")
        db.close()

def get_data_horaire_from_api():

    """
    Récupère les données de consommation au pas de temps demie-heure pour un compteur (PRM)
    entre les dates start (incluse) et end (exclue).
    
    :param start: date de début au format 'YYYY-MM-DD'
    :param end: date de fin (non incluse) au format 'YYYY-MM-DD'
    :return: réponse JSON si succès, sinon lève une exception
    """
    from datetime import datetime, timedelta
    import os
    import logging


    # Récupérer les variables d'environnement avec des valeurs par défaut
    logger.info("début appel API")
    API_TOKEN = os.environ.get("API_TOKEN_ELEC", "")
    PRM       = os.environ.get("PRM_ELEC", "")


    today_tstamp = datetime.now()
    day_start_import_tstamp = (today_tstamp - timedelta(days=2))

    today_str = today_tstamp.strftime('%Y-%m-%d')
    day_start_import_str = day_start_import_tstamp.strftime('%Y-%m-%d') 


    base_url = "https://conso.boris.sh/api/consumption_load_curve"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "User-Agent": "MonApp/1.0 (contact@example.com)"  # optionnel mais recommandé
    }
    params = {
        "prm": PRM,
        "start": day_start_import_str,
        "end": today_str
    }
    
    response = requests.get(base_url, headers=headers, params=params)
    # Vérifier le code HTTP
    if response.status_code != 200:
        raise Exception(f"Erreur HTTP {response.status_code} : {response.text}")
    logger.info("fin appel API")
    return response.json()
