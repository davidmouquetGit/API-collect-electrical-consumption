# API collecte données de consommations électricité/gaz/météo

## Objectif

Cette API a pour objectif de collecter toutes les 24 heures les données d'un logement particulier:
- de consommation horaire d'électricité
- de consommation journalière de gaz naturel
- de température extérieur

puis de les stocker dans une base de données. Cette base de données dessert ensuite une application de suivi des consommations.

L'architecture de l'API est représentée ci-dessous. GRDF ne fournit apparemment pas d'API pour les clients particuliers. les données de consommations de gaz sont téléchargées manuellement et poussées vers un bucket.

![Architecture](images/architectureapi.png)

## 📊 Sources utilisées

- API météo [OpenMeteo](https://pypi.org/project/openmeteo-requests/)
- API [Linky](https://conso.boris.sh/)   
- Données client GRDF  


## ⚙️ Technologie utilisées

- RDS AWS pour le stockage des données dans une base PostgreSQL
- S3 AWS pour le stockage des données GRDF
- EC2 AWS pour l'hébergement de l'API sur un serveur virtuel
- Python pour le code avec:
  - FastAPI pour le framework de l'API
  - apscheduler pour les appels quotidients des API météo et Linky
  - sqlalchemy pour l'insertion et la gestion des données vers PostgreSQL
- Docker pour le déploiement de l'API sur EC2

## 🗂️ Installation

- Prérequis
  - Disposer d'un compte AWS (Free-Tiers est suffisant)
  - Avoir créé un bucket sur AWS/S3
  - Avoir créé une base de donnée PostgreSQL dans AWS/Aurora RDS
  - Avoir créé une instance AWS/EC2
  - Autoriser l'accès de l'instance EC2 vers la base de données
  - Disposer d'une clé pour l'accès à l'API ENEDIS
- Création d'un environnement virtuel python et installation des librairies
- Paramétrer un fichier .env renseignant les variables d'environnement

| Variable       | Description       |
|-----------------|-----------------|
| PRM_ELEC | N° du point de comptage Linky (14 chiffres) |
| API_CONSO_URL | https://conso.boris.sh/api/consumption_load_curve |
| API_TOKEN | token de l'API ci-dessus |
| NOM_DU_BUCKET | chemin d'accès vers le bucket S3|
| aws_access_key_id | clés d'accès vers bucket S3 |
| aws_secret_access_key | clés d'accès secrète vers bucket S3 |
| DB_USER | nom d'utilisateur PostgreSQL (souvent "postgres") |
| DB_PASSWORD | mot de passe PostgreSQL|
| DB_HOST | point de terminaison de la base PostgreSQL|
| DB_PORT | port PostgreSQL (5432)|
| API_METEO_URL | https://archive-api.open-meteo.com/v1/archive|
| LATITUDE | Latitude de la station (nombre décimal)|
| LONGITUDE | Longitude de la station (nombre décimal)|

- Construire l'image docker et lancer le conteneur
  -  docker compose up -d --build
