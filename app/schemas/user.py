from pydantic import BaseModel  # validazione dati

class UserCreate(BaseModel):
    nome: str
    email: str
    password: str
    ruolo: str

class UserLogin(BaseModel):
    email: str
    password: str