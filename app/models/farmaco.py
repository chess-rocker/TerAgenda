from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Farmaco(Base):
    __tablename__ = "farmaci"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    descrizione = Column(String)