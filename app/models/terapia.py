from sqlalchemy import Column, Integer, Date, String, Boolean, ForeignKey
from app.db.database import Base

class Terapia(Base):
    __tablename__ = "terapie"

    id = Column(Integer, primary_key=True, index=True)
    paziente_id = Column(Integer, ForeignKey("users.id"))
    medico_id = Column(Integer, ForeignKey("users.id"))

    data_inizio = Column(Date)
    data_fine = Column(Date)

    frequenza_giornaliera = Column(Integer)
    
    note = Column(String)

    firmata = Column(Boolean, default=False)
    firma_digitale = Column(String, nullable=True)