from passlib.context import CryptContext # libreria per hash password
from datetime import datetime, timedelta
import jwt  # PyJWT - creazione/verifica token di accesso

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)# trasforma la password in hash

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password) # confronto login


# ===================== AUTENTICAZIONE (JWT) =====================
# NOTA: in produzione la SECRET_KEY va letta da variabile d'ambiente
# (es. os.environ["SECRET_KEY"]) e mai tenuta hardcoded nel codice.
SECRET_KEY = "teragenda-dev-secret-key-cambiami-in-produzione"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8  # 8 ore


def create_access_token(user_id: int, ruolo: str) -> str:
    """Crea un token firmato contenente id utente, ruolo e scadenza."""
    scadenza = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "ruolo": ruolo,
        "exp": scadenza
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Decodifica e verifica il token. Solleva jwt.PyJWTError se non valido/scaduto."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])