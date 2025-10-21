from app.models import ConsoHeureElec, ConsoJourElec, ConsoJourGaz
from sqlalchemy.exc import IntegrityError
import logging
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Créer un gestionnaire de fichier (FileHandler) qui écrit dans un fichier
file_handler = logging.FileHandler('/var/log/myapp/app.log')
file_handler.setLevel(logging.INFO)

# Créer un format pour les logs
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Ajouter le gestionnaire de fichier au logger
logger.addHandler(file_handler)





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
            return False

    # Upsert (INSERT or UPDATE)
    try:
        stmt = insert(ConsoHeureElec).values(data_to_insert)
        stmt = stmt.on_conflict_do_update(
            index_elements=["horodatage"],  # correspond à UNIQUE (horodatage)
            set_={"value": stmt.excluded.value}  # met à jour la valeur
        )

        db.execute(stmt)
        db.commit()
        logger.info(f"{len(data_to_insert)} lignes insérées ou mises à jour avec succès dans conso horaire.")

    except IntegrityError as e:
        db.rollback()
        logger.error(f"Erreur d'intégrité conso horaire: {e}")
        return False
    except Exception as e:
        db.rollback()
        logger.error(f"Erreur d'insertion conso horaire: {e}")
        return False
    
    return True


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
            return f"Erreur de format sur l'enregistrement journalier"

    
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
        logger.error(f"Erreur d'intégrité données jours: {e}")
        return f"Erreur d'intégrité données jours: {e}"
    except Exception as e:
        db.rollback()
        logger.error(f"Erreur d'insertion données jours: {e}")
        return f"Erreur d'insertion données jours: {e}"
    
    return "OK"

    

def insert_data_conso_gaz_jour(db, df):
    import pandas as pd
    

    data_to_insert = []

    # Prépare les données
    for idx_, row in df.iterrows():
        try:
            data_to_insert.append({"horodatage":row['horodatage'], "volume": row['volume'], "energie": row['energie'], "pci": row['pci'], "text": row['text']})
        except Exception as e:
            logger.warning(f"Erreur de format sur l'enregistrement journalier données gaz")
            return f"Erreur de format sur l'enregistrement journalier données gaz"


    # Upsert (INSERT or UPDATE)
    try:
        stmt = insert(ConsoJourGaz).values(data_to_insert)
        stmt = stmt.on_conflict_do_update(
            index_elements=["horodatage"],  # correspond à UNIQUE (horodatage)
            set_={"energie": stmt.excluded.energie}  # met à jour la valeur
        )

        db.execute(stmt)
        db.commit()
        logger.info(f"{len(data_to_insert)} lignes insérées ou mises à jour avec succès sur les données gaz jours.")

    except IntegrityError as e:
        db.rollback()
        logger.error(f"Erreur d'intégrité données gaz jours: {e}")
        return f"Erreur d'intégrité données gaz jours: {e}"
    except Exception as e:
        db.rollback()
        logger.error(f"Erreur d'insertion données gaz jours: {e}")
        return f"Erreur d'insertion données gaz jours: {e}"
    return "OK"