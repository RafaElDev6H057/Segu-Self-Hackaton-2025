# core/security.py

from passlib.context import CryptContext

# Creamos una instancia de CryptContext, especificando el esquema de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con una hasheada.
    """
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    """
    Hashea una contraseña en texto plano.
    """
    return pwd_context.hash(password)