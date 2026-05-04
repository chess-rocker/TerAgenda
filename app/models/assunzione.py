from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db.database import Base
from enum import Enum

class StatoAssunzione(str, Enum):
    DA_PRENDERE = "DA_PRENDERE"
    PRESA = "PRESA"
    SALTATA = "SALTATA"
    
class Assunzione(Base):
    __tablename__ = "assunzioni"

    id = Column(Integer, primary_key=True, index=True)
    terapia_id = Column(Integer, ForeignKey("terapie.id"))
    farmaco_id = Column(Integer, ForeignKey("farmaci.id"))

    orario = Column(DateTime)
    dosaggio = Column(String)

    stato = Column(String, default=StatoAssunzione.DA_PRENDERE)  # DA_PRENDERE, PRESA, SALTATA
