from sqlalchemy import create_engine  # crea la connessione al database
from sqlalchemy.orm import sessionmaker, declarative_base  # gestione sessioni e base dei modelli

# URL del database (SQLite locale)
DATABASE_URL = "sqlite:///./teragenda.db"

# crea il motore di connessione al database
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # necessario per FastAPI
)

# crea sessioni per comunicare con il database
SessionLocal = sessionmaker(
    autocommit=False,   # non salva automaticamente
    autoflush=False,    # evita query automatiche non volute
    bind=engine         # collega al database
)

# base da cui erediteranno tutti i modelli (tabelle)
Base = declarative_base()