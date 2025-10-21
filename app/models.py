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


    horodatage = Column(TIMESTAMP, nullable=False, primary_key=True)
    value = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint("horodatage", name="conso_jour_elec_horodatage_key"),
    )

    def __repr__(self):
        return f"<ConsoJourElec(horodatage={self.horodatage}, value={self.value})>"
    

class ConsoJourGaz(Base):
    __tablename__ = "conso_jour_gaz"

    horodatage = Column(TIMESTAMP, nullable=False, primary_key=True)
    volume = Column(Float, nullable=True)
    energie = Column(Float, nullable=True)
    pci = Column(Float, nullable=True)
    text = Column(Float, nullable=True)


    __table_args__ = (
        UniqueConstraint("horodatage", name="conso_jour_gaz_horodatage_key"),
    )

    def __repr__(self):
        return f"<ConsoJourGaz(id={self.id}, horodatage={self.horodatage}, value={self.volume})>"
    
