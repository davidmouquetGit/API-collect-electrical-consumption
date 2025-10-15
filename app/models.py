from sqlalchemy import Column, Integer, Float, DateTime
from app.db import Base

class Conso(Base):
    __tablename__ = "courbecharge"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    value = Column(Float)
