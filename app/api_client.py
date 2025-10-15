from app.config import API_TOKEN, PRM
import requests
import cloudscraper




def get_consumption_load(start: str, end: str):
    """
    Récupère les données de consommation au pas de temps demie-heure pour un compteur (PRM)
    entre les dates start (incluse) et end (exclue).
    
    :param start: date de début au format 'YYYY-MM-DD'
    :param end: date de fin (non incluse) au format 'YYYY-MM-DD'
    :return: réponse JSON si succès, sinon lève une exception
    """

    scraper = cloudscraper.create_scraper()

    base_url = "https://conso.boris.sh/api/consumption_load_curve"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "User-Agent": "MonApp/1.0 (contact@example.com)"  # optionnel mais recommandé
    }
    params = {
        "prm": PRM,
        "start": start,
        "end": end
    }
    
    response = requests.get(base_url, headers=headers, params=params)
    # Vérifier le code HTTP
    if response.status_code != 200:
        raise Exception(f"Erreur HTTP {response.status_code} : {response.text}")
    
    return response.json()