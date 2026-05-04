from passlib.context import CryptContext # libreria per hash password

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)# trasforma la password in hash

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password) # confronto login