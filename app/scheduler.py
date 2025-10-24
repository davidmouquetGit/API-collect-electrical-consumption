
from apscheduler.schedulers.background import BackgroundScheduler


from app.db import SessionLocal
from app.crud import insert_data_conso_horaire, insert_data_conso_jour, insert_data_meteo_jour
import requests
import logging
from app.collecte_meteo_data import get_meteo_data

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Créer un gestionnaire de fichier (FileHandler) qui écrit dans un fichier
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)

# Créer un format pour les logs
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Ajouter le gestionnaire de fichier au logger
logger.addHandler(file_handler)



def start_scheduler():
    logger.info("Début scheduler")
    scheduler = BackgroundScheduler()
    scheduler.add_job(collect_data, "interval", hours=24)
    scheduler.start()
    print("Scheduler lancé (toutes les 24 h)")


def collect_data():
    logger.info("Début collect data conso horaire")
    db = SessionLocal()
    try:
        data = get_data_horaire_from_api()
        data = data["interval_reading"]
        insert_data_conso_horaire(db, data)
        insert_data_conso_jour(db, data)

        #df_conso_gaz = get_data_jour_gaz_from_s3()  --> les données de conso gaz sont désormais injectée directement dasn streamlit
        #insert_data_conso_gaz_jour(db, df_conso_gaz)
        df_meteo = get_meteo_data()
        if df_meteo is not None:
            insert_data_meteo_jour(db, df_meteo)
        
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
    from dotenv import load_dotenv

    load_dotenv()


    # Récupérer les variables d'environnement avec des valeurs par défaut
    logger.info("début appel API")

    API_TOKEN = os.environ.get("API_TOKEN", "")
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
	print(PRM)
	print(day_start_import_str)
	print(today_str)

        raise Exception(f"Erreur HTTP {response.status_code} : {response.text}")
    logger.info("fin appel API")
    return response.json()




def get_data_jour_gaz_from_s3():
    import pandas as pd

    liste_excel = lister_fichiers_excel_s3()
    list_df = list()

    for f in liste_excel:
        print(f"Lecture du fichier : {f}")
        df = lire_fichier_excel_s3(f)
        list_df.append(df)
    
    df_newdata_gaz = pd.concat(list_df)
    df_newdata_gaz = df_newdata_gaz[['Date de relevé', 'Volume consommé (m3)', 'Energie consommée (kWh)', 'Coefficient de conversion', 'Température locale (°C)']]
    df_newdata_gaz.columns = ['horodatage', 'volume', 'energie','pci','text']
    df_newdata_gaz['horodatage']=pd.to_datetime(df_newdata_gaz['horodatage'], format='%d/%m/%Y')

    return df_newdata_gaz

def lire_fichier_excel_s3(fichier_s3):

    import boto3
    import os
    import awswrangler as wr

    from dotenv import load_dotenv

    load_dotenv()

    # Créez une session boto3 avec vos identifiants
    session = boto3.Session(
        aws_access_key_id=os.environ.get("aws_access_key_id"),
        aws_secret_access_key=os.environ.get("aws_secret_access_key")
    )

    try:
        # Lisez le fichier Excel avec awswrangler
        df = wr.s3.read_excel(
            path=fichier_s3,
            boto3_session=session,
            sheet_name=0,
            skiprows=8,
            usecols="B:H"
        )
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        df = None

    return df    

def lister_fichiers_excel_s3():
    """
    Récupère la liste des fichiers Excel (.xlsx, .xls) dans un bucket S3.

    :return: Une liste des clés (noms de chemins) des fichiers Excel.
    """
    import os
    import boto3

    from dotenv import load_dotenv

    load_dotenv()

    bucket_name   = os.environ.get("NOM_DU_BUCKET")
    prefix        = os.environ.get("PREFIXE_DOSSIER")  

    s3 = boto3.client(
        's3',
        aws_access_key_id     = os.environ.get("aws_access_key_id"),
        aws_secret_access_key = os.environ.get("aws_secret_access_key")
    )

    
    excel_files = []
    
    # Pour gérer un grand nombre de fichiers (pagination)
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    for page in pages:
        if 'Contents' in page:
            for obj in page['Contents']:
                key = obj['Key']
                # Filtrer par extension
                if key.lower().endswith('.xlsx') or key.lower().endswith('.xls'):                    
                    excel_files.append(f"s3://{bucket_name}/{key}")
                    
    return excel_files
