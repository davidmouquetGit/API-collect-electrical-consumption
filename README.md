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


## Reconstruire l'image docker
docker build -t apigetdataconso .


## Relancer le conteneur
docker run -d --name apigetdataconso \
  -e API_TOKEN=eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NjAyNjMyNTksImV4cCI6MTg1NDc4NDg1OSwic3ViIjpbIjAyMjk3MjUwMzI2MzYwIl19.N0tP2NOkYwmCzFRo4tbxxfnS7OGMdRpc2p6v8zs2Pmo \
  -e PRM=02297250326360 \
  -e DB_USER=postgres \
  -e DB_PASSWORD=Labrax_007 \
  -e DB_HOST=conso.cr2m0qmgsjvc.eu-north-1.rds.amazonaws.com \
  -e DB_PORT=5432 \
  -e DB_NAME=conso \
  -p 8000:8000 apigetdataconso

## Adresse API

http://13.51.36.207:8000/