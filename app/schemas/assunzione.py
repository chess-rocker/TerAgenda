from enum import Enum
from pydantic import BaseModel
from datetime import datetime

class AssunzioneCreate(BaseModel):
    terapia_id: int
    orario: datetime
    dosaggio: str

class StatoAssunzione(str, Enum):
    DA_PRENDERE = "DA_PRENDERE"
    PRESA = "PRESA"
    SALTATA = "SALTATA"

class AssunzioneUpdate(BaseModel):
    stato: StatoAssunzione