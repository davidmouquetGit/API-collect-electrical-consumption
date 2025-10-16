from app.models import Conso
from app.models import CourbeCharge
from sqlalchemy.exc import IntegrityError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def insert_data(db, records):
    pass



def insert_data_conso_horaire(db, records):
    """Insère les données de consomation horaire la base (évite les doublons)."""
    from datetime import datetime

    for record in records:
        try:
            value_float = float(record['value'])
            ts = datetime.strptime(record['date'], '%Y-%m-%d %H:%M:%S')
            db.add(CourbeCharge(timestamp=ts, value=value_float))
            db.commit()
	    logger.info("insertion data ok")
        except IntegrityError:
            db.rollback()
            logger.info("inserion data echec")



