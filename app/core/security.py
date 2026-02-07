from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def hash_password(password: str) -> str:
    safe_password = password[:72]
    return pwd_context.hash(safe_password)

def verify_password(password: str, hashed: str) -> bool:
    safe_password = password[:72]
    return pwd_context.verify(safe_password, hashed)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

