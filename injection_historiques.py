from app.db import Base, engine, SessionLocal
from sqlalchemy import Column, Integer, Float, TIMESTAMP, UniqueConstraint
from sqlalchemy.dialects.postgresql import insert


class MeteoJour(Base):
    __tablename__ = "meteo_jour"

    horodatage = Column(TIMESTAMP, primary_key=True, nullable=False)
    temperature_2m_min = Column(Float, nullable=False)
    temperature_2m_max = Column(Float, nullable=False)
    __table_args__ = (
        UniqueConstraint("horodatage", name="uq_meteo_day_horodatage"),
    )



# Crée les tables
Base.metadata.create_all(bind=engine)


def insert_meteo_from_csv(csv_path: str):
    """Insère les données météo d’un CSV dans la table meteo_jour."""
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

if __name__ == "__main__":
    # Exemple d'utilisation
    insert_meteo_from_csv("data/daily_temperature_data.csv")
    