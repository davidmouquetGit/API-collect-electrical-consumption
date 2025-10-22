import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta



def get_meteo_data():

    try:

        # Charger le fichier .env
        load_dotenv()

        # Lecture et conversion en float
        LATITUDE = float(os.getenv("LATITUDE"))
        LONGITUDE = float(os.getenv("LONGITUDE"))
        url = os.getenv("API_METEO_URL")
        if not LATITUDE or not LONGITUDE or not url:
            raise ValueError("LATITUDE, LONGITUDE ou API_METEO_URL manquante dans le fichier .env")
        
        if not (-90 <= LATITUDE <= 90):
            raise ValueError(f"Latitude invalide : {LATITUDE}")
        if not (-180 <= LONGITUDE <= 180):
            raise ValueError(f"Longitude invalide : {LONGITUDE}")

        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        openmeteo = openmeteo_requests.Client(session = retry_session)

        

        today_tstamp = datetime.now()
        day_start_import_tstamp = (today_tstamp - timedelta(days=7))

        today_str = today_tstamp.strftime('%Y-%m-%d')
        day_start_import_str = day_start_import_tstamp.strftime('%Y-%m-%d') 


        params = {
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
            "start_date": day_start_import_str,
            "end_date": today_str,
            "daily": ["temperature_2m_min", "temperature_2m_max"],
            "timezone": "GMT",
        }
        responses = openmeteo.weather_api(url, params=params)
        if not responses:
            raise RuntimeError("Aucune réponse reçue de l'API météo")

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]


        # Process daily data. The order of variables needs to be the same as requested.
        daily = response.Daily()
        daily_temperature_2m_min = daily.Variables(0).ValuesAsNumpy()
        daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()

        daily_data = {"date": pd.date_range(
            start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
            end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = daily.Interval()),
            inclusive = "left"
        )}

        daily_data["temperature_2m_min"] = daily_temperature_2m_min
        daily_data["temperature_2m_max"] = daily_temperature_2m_max

        daily_dataframe = pd.DataFrame(data = daily_data)
        daily_dataframe["date"] = daily_dataframe["date"].dt.tz_localize(None)

        daily_dataframe.columns = ["horodatage", "temperature_2m_min", "temperature_2m_max"]


        return daily_dataframe
    
    except Exception as e:
        print(f"Erreur dans get_meteo_data : {type(e).__name__} - {e}")
        return None