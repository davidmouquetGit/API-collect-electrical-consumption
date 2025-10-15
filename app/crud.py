from app.models import Conso
from sqlalchemy.exc import IntegrityError

def insert_data(db, records):
    """Insère les données simulées dans la base (évite les doublons)."""
    for record in records:
        try:
            db.add(Conso(timestamp=record["timestamp"], value=record["value"]))
            db.commit()
        except IntegrityError:
            db.rollback()
