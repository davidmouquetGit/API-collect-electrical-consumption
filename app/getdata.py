from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
import os
load_dotenv()



def get_data(source = "elec_hour"):
    
    """
    Retourne les données depuis la base postgresql.

    Args:
        source (str): identifiant parmis
            "elec_hour"
            "elec_jour"
            "gaz_jour"
            "meteo_jour"

    Returns:
        data frame horodaté
    """

    if source not in ["elec_hour", "elec_jour","gaz_jour","meteo_jour"]:
        print("source de données inconnue")

    match source:

        case "elec_hour":
            sql_request = "SELECT horodatage, value FROM conso_heure_elec"

        case "elec_jour":
            sql_request = "SELECT horodatage, value FROM conso_jour_elec"

        case "gaz_jour":
            sql_request = "SELECT horodatage, energie FROM conso_jour_gaz"

        case "meteo_jour":
            sql_request =  "SELECT horodatage, temperature_2m_min, temperature_2m_max FROM meteo_jour"

    
   
    DB_URL = os.getenv("DB_URL")
    engine = create_engine(DB_URL)
    # Lire un DataFrame
    df = pd.read_sql(sql_request, engine)
    df.index = df['horodatage']
    df = df.sort_index()

    return df

