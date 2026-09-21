from pydantic import BaseModel  # validazione dati

class UserCreate(BaseModel):
    nome: str
    email: str
    password: str
    ruolo: str

class UserLogin(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    """Corpo della risposta di /login, così Swagger la documenta correttamente."""
    message: str
    user_id: int
    ruolo: str
    access_token: str
    token_type: str