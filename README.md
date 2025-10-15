# API-collect-electrical-consumption
API pour collecter les données de consommations électrique d'ENEDIS

## se connecter à une bdd "conso" sur EC2

psql -h conso.cr2m0qmgsjvc.eu-north-1.rds.amazonaws.com -p 5432 -U postgres -d conso

## Définir les variables d’environnement sur EC2

### Éditer le fichier .bashrc
nano ~/.bashrc

### Ajouter les lignes suivantes à la fin du fichier
export DB_ENDPOINT="conso.cr2m0qmgsjvc.eu-north-1.rds.amazonaws.com"
export DB_PORT="5432"
export DB_NAME="conso"
export DB_USER="postgres"
export DB_PASSWORD="ton_mot_de_passe"

### Charger les variables
source ~/.bashrc

### Test python connection

import os
import psycopg2

db_endpoint = os.environ.get("DB_ENDPOINT")
db_port = os.environ.get("DB_PORT")
db_name = os.environ.get("DB_NAME")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")

try:
    conn = psycopg2.connect(
        host=db_endpoint,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=db_password
    )
    print("Connexion réussie à la base de données !")
    conn.close()
except Exception as e:
    print(f"Erreur de connexion : {e}")
