from app.db import Base, engine, SessionLocal
from sqlalchemy import Column, Integer, Float,String, TIMESTAMP, UniqueConstraint
from sqlalchemy.dialects.postgresql import insert
from app.models import Occupation


# Crée les tables
Base.metadata.create_all(bind=engine)

def insert_data_occupation():
    from app.crud import insert_data_occup_jour
    from app.db import SessionLocal
    from app.db import Base, engine 

    db = SessionLocal()


    Base.metadata.create_all(bind=engine)

    insert_data_occup_jour(db)

    db.close()

"""


def insert_meteo_from_csv(csv_path: str):
    import pandas as pd

    # --- 2️Lecture du CSV avec pandas ---
    df = pd.read_csv(csv_path, sep=",")
    print(f"Lecture de {len(df)} lignes depuis {csv_path}")

    # --- Vérification des colonnes attendues ---
    required_cols = {"date", "temperature_2m_min", "temperature_2m_max"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Colonnes manquantes dans le CSV : {', '.join(missing)}")

    # --- Renommage pour correspondre au modèle SQLAlchemy ---
    df = df.rename(columns={"date": "horodatage"})

    # --- Conversion de la colonne date ---
    df["horodatage"] = pd.to_datetime(df["horodatage"])

    # --- Création de la session SQLAlchemy ---
    session = SessionLocal()

    try:
        # --- Préparation de la requête d'insertion ---
        stmt = insert(MeteoJour).values(df[["horodatage", "temperature_2m_min", "temperature_2m_max"]].to_dict(orient="records"))

        # --- 8Gestion des doublons (ignore si horodatage existe déjà) ---
        stmt = stmt.on_conflict_do_nothing(index_elements=["horodatage"])

        # --- Exécution et validation ---
        result = session.execute(stmt)
        session.commit()

        print(f"{result.rowcount} lignes insérées (les doublons ont été ignorés).")

    except Exception as e:
        session.rollback()
        print(f"Erreur lors de l'insertion : {e}")
        raise

    finally:
        session.close()
"""
if __name__ == "__main__":
    # Exemple d'utilisation
    insert_data_occupation()
    