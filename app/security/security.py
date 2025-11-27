from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

MAX_BCRYPT_BYTES = 72  # Limite bcrypt

def get_password_hash(password: str):
    # SHA-256 -> bytes
    sha256_bytes = hashlib.sha256(password.encode()).digest()
    # tronquer si nécessaire à 72 bytes
    truncated = sha256_bytes[:MAX_BCRYPT_BYTES]
    return pwd_context.hash(truncated)

def verify_password(plain_password, hashed_password):
    sha256_bytes = hashlib.sha256(plain_password.encode()).digest()
    truncated = sha256_bytes[:MAX_BCRYPT_BYTES]
    return pwd_context.verify(truncated, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def decode_token(token: str):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    return payload
