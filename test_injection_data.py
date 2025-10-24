import sys, os

from dotenv import load_dotenv
import pytest
from app.crud import insert_data_conso_jour, insert_data_conso_horaire, insert_data_meteo_jour, insert_data_occup_jour
from app.scheduler import get_data_horaire_from_api
from app.db import SessionLocal
from app.collecte_meteo_data import get_meteo_data


class TestDataInsertion:
    @pytest.fixture(autouse=True)
    def setup(self):
        # Charger le fichier .env
        load_dotenv()
        # Récupérer les variables d'environnement
        self.API_TOKEN = os.environ.get("API_TOKEN", "")
        self.PRM = os.environ.get("PRM_ELEC", "")
        assert self.API_TOKEN != "", "API_TOKEN is empty"
        assert self.PRM != "", "PRM_ELEC is empty"
        assert len(self.PRM) == 14, "PRM_ELEC length is not 14"

        DB_USER = os.getenv("DB_USER", "")
        DB_PASSWORD = os.getenv("DB_PASSWORD", "")
        DB_HOST = os.getenv("DB_HOST", "")
        DB_PORT = os.getenv("DB_PORT", "")
        DB_NAME = os.getenv("DB_NAME", "conso")

        assert DB_USER == "postgres", "DB_USER is incorrect"
        assert len(DB_PASSWORD) >= 5, "DB_PASSWORD is incorrect"
        assert DB_NAME == "conso", "data base name is incorrect"

        self.aws_access_key_id = os.environ.get("aws_access_key_id", "")
        self.aws_secret_access_key = os.environ.get("aws_secret_access_key", "")
        self.NOM_DU_BUCKET = os.environ.get("NOM_DU_BUCKET", "")
        self.PREFIXE_DOSSIER = os.environ.get("PREFIXE_DOSSIER", "")
        assert self.aws_access_key_id != "", "aws_access_key_id is empty"
        assert self.aws_secret_access_key != "", "aws_secret_access_key is empty"
        assert self.NOM_DU_BUCKET != "", "NOM_DU_BUCKET is empty"
        assert self.PREFIXE_DOSSIER != "", "PREFIXE_DOSSIER is empty"
    

    @pytest.fixture
    def data_elec_horaire(self):
        data = get_data_horaire_from_api()
        assert data is not None, "Pas de données horaire électrique retournées"
        assert "interval_reading" in data, "interval_reading key not in response"
        data = data["interval_reading"]
        assert len(data) > 0, "Aucune donnée horaire électrique dans interval_reading"
        return data

    def test_get_data_elec_horaire(self, data_elec_horaire):
        assert len(data_elec_horaire) > 0

    def test_insert_data_conso_heure(self, data_elec_horaire):
        db = SessionLocal()
        result = insert_data_conso_horaire(db, data_elec_horaire)
        assert result is True, "L'insertion des données a échoué"
        db.close()

    def test_insert_data_conso_jour(self, data_elec_horaire):
        db = SessionLocal()
        result = insert_data_conso_jour(db, data_elec_horaire)
        assert result=="OK", "L'insertion des données journalières a échoué"
        db.close()

    def test_insert_data_occup_jour(self):
        db = SessionLocal()
        result = insert_data_occup_jour(db)
        assert result=="OK", "L'insertion des données occupation a échoué"
        db.close()


    def test_get_meteo_data(self):
        db = SessionLocal()
        data = get_meteo_data()
        assert data is not None, "Pas de données météo retournées"
        result = insert_data_meteo_jour(db, data)
        assert result=="OK", result
        db.close()