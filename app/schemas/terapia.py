from pydantic import BaseModel
from datetime import date

class TerapiaCreate(BaseModel):
    paziente_id: int
    medico_id: int
    farmaco_id: int | None = None  # ora propagato alle assunzioni generate
    data_inizio: date
    data_fine: date
    frequenza_giornaliera: int
    note: str | None = None


class TerapiaFirma(BaseModel):
    """Corpo vuoto: la firma usa solo i dati già presenti sulla terapia + l'utente autenticato."""
    pass