from app.models import ConsoHeureElec, ConsoJourElec
from sqlalchemy.exc import IntegrityError
import logging
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def insert_data_conso_horaire(db, records):
    """
    Insère les données horaires dans la base PostgreSQL.
    Si un horodatage existe déjà, la valeur est mise à jour (upsert).
    """
    data_to_insert = []

    # Prépare les données
    for record in records:
        try:
            value_float = float(record["value"])
            ts = datetime.strptime(record["date"], "%Y-%m-%d %H:%M:%S")
            data_to_insert.append({"horodatage": ts, "value": value_float})
        except Exception as e:
            logger.warning(f"Erreur de format sur l'enregistrement {record} : {e}")

    # Upsert (INSERT or UPDATE)
    try:
        stmt = insert(ConsoHeureElec).values(data_to_insert)
        stmt = stmt.on_conflict_do_update(
            index_elements=["horodatage"],  # correspond à UNIQUE (horodatage)
            set_={"value": stmt.excluded.value}  # met à jour la valeur
        )

        db.execute(stmt)
        db.commit()
        logger.info(f"{len(data_to_insert)} lignes insérées ou mises à jour avec succès.")

    except IntegrityError as e:
        db.rollback()
        logger.error(f"Erreur d'intégrité : {e}")
    except Exception as e:
        db.rollback()
        logger.error(f"Erreur d'insertion : {e}")


def insert_data_conso_jour(db, records):
    import pandas as pd
    df = pd.DataFrame(records)
    df['date'] = pd.to_datetime(df['date'])
    df['value'] = df['value'].astype(float)
    df.index = df['date']
    conso_jour = df['value'].resample('D').mean()/1000*24

    data_to_insert = []

    # Prépare les données
    for ts, value in conso_jour.items():
        try:
            data_to_insert.append({"horodatage": ts, "value": value})
        except Exception as e:
            logger.warning(f"Erreur de format sur l'enregistrement journalier")

    
    # Upsert (INSERT or UPDATE)
    try:
        stmt = insert(ConsoJourElec).values(data_to_insert)
        stmt = stmt.on_conflict_do_update(
            index_elements=["horodatage"],  # correspond à UNIQUE (horodatage)
            set_={"value": stmt.excluded.value}  # met à jour la valeur
        )

        db.execute(stmt)
        db.commit()
        logger.info(f"{len(data_to_insert)} lignes insérées ou mises à jour avec succès sur les données jours.")

    except IntegrityError as e:
        db.rollback()
        logger.error(f"Erreur d'intégrité : {e}")
    except Exception as e:
        db.rollback()
        logger.error(f"Erreur d'insertion : {e}")