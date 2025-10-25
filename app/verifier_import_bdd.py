from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
import os


load_dotenv()

# Récupérer les variables d'environnement avec des valeurs par défaut
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "conso")


# Construire l'URL de connexion à la base de données
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"DB_URL: {DB_URL}")  # Ajout d'un print pour débogage

# Créer l'engin SQLAlchemy
engine = create_engine(DB_URL)


# Lire un DataFrame
df = pd.read_sql("SELECT horodatage, value FROM conso_heure_elec order by horodatage desc", engine)
print("conso elec horaire\n",df.head())

df = pd.read_sql("SELECT horodatage, value FROM conso_jour_elec order by horodatage desc", engine)
print("conso elec jour\n",df.head())

df = pd.read_sql("SELECT horodatage, energie FROM conso_jour_gaz order by horodatage desc", engine)
print("conso gaz jour\n",df.head())

df = pd.read_sql("SELECT * FROM meteo_jour order by horodatage desc", engine)
print("meteo jour\n",df.head())