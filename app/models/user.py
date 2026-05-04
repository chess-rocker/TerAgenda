from sqlalchemy import Column, Integer, String, DateTime  # tipi colonne database
from datetime import datetime  # per timestamp creazione/modifica
from app.db.database import Base  # base del database

# definizione tabella utenti
class User(Base):
    __tablename__ = "users"  # nome tabella nel database

    id = Column(Integer, primary_key=True, index=True)  # ID univoco utente

    nome = Column(String, nullable=False)  # nome obbligatorio

    email = Column(
        String,
        unique=True,  # email non duplicabili
        index=True,   # ricerca veloce
        nullable=False
    )

    password_hash = Column(String, nullable=False)  # password salvata in modo sicuro (hash)

    ruolo = Column(String, nullable=False)  # paziente / medico / admin

    created_at = Column(DateTime, default=datetime.utcnow)  # data creazione
    updated_at = Column(DateTime, default=datetime.utcnow)  # ultima modifica