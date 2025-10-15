from app.models import Conso
from app.models import CourbeCharge
from sqlalchemy.exc import IntegrityError

def insert_data(db, records):
    """Insère les données simulées dans la base (évite les doublons)."""
    for record in records:
        try:
            db.add(Conso(timestamp=record["timestamp"], value=record["value"]))
            db.commit()
        except IntegrityError:
            db.rollback()



def insert_data_conso_horaire(db, records):
    """Insère les données de consomation horaire la base (évite les doublons)."""
    from datetime import datetime

    for record in records:
        try:
            value_float = float(record['value'])
            ts = datetime.strptime(record['date'], '%Y-%m-%d %H:%M:%S')
            db.add(CourbeCharge(timestamp=ts, value=value_float))
            db.commit()
        except IntegrityError:
            db.rollback()
