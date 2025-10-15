import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
PRM = os.getenv("PRM")
DB_URL = os.getenv("DB_URL", "postgresql+psycopg2://user:password@localhost/conso")

