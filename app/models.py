from app.db import Base
from sqlalchemy import Column, Integer, Float, TIMESTAMP, UniqueConstraint


class ConsoHeureElec(Base):
    __tablename__ = "conso_heure_elec"

    id = Column(Integer, primary_key=True, autoincrement=True)
    horodatage = Column(TIMESTAMP, nullable=False)
    value = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint("horodatage", name="uq_conso_heure_elec_horodatage"),
    )

    def __repr__(self):
        return f"<ConsoHeureElec(id={self.id}, horodatage={self.horodatage}, value={self.value})>"
    

class ConsoJourElec(Base):
    __tablename__ = "conso_jour_elec"

    id = Column(Integer, primary_key=True, autoincrement=True)
    horodatage = Column(TIMESTAMP, nullable=False)
    value = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint("horodatage", name="uq_conso_jourelec_horodatage"),
    )

    def __repr__(self):
        return f"<ConsoJourElec(id={self.id}, horodatage={self.horodatage}, value={self.value})>"
    
