from sqlalchemy import Column, DateTime, Float
from app.db import Base

class Conso(Base):
    __tablename__ = "conso"

    timestamp = Column(DateTime, primary_key=True)
    value = Column(Float, nullable=False)
