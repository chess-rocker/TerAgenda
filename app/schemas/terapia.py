from pydantic import BaseModel
from datetime import date

class TerapiaCreate(BaseModel):
    paziente_id: int
    medico_id: int
    data_inizio: date
    data_fine: date
    frequenza_giornaliera: int
    note: str | None = None