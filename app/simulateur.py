import random
from datetime import datetime

def generate_fake_data(n=1):
    """Génère n points aléatoires simulés."""
    data = []
    for _ in range(n):
        record = {
            "timestamp": datetime.now(),
            "value": round(random.uniform(0.5, 5.0), 3)  # kWh aléatoires
        }
        data.append(record)
    return data
