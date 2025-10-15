from sqlalchemy import Column, DateTime, Float
from app.db import Base

class Conso(Base):
    __tablename__ = "conso"

    timestamp = Column(DateTime, primary_key=True)
    value = Column(Float, nullable=False)


class CourbeCharge(Base):
    __tablename__ = "consohoraire"

    timestamp = Column(DateTime, primary_key=True)
    value = Column(Float, nullable=False)


