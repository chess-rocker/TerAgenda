from pydantic import BaseModel

class FarmacoCreate(BaseModel):
    nome: str
    descrizione: str | None = None


class FarmacoResponse(BaseModel):
    id: int
    nome: str
    descrizione: str | None = None

    class Config:
        from_attributes = True