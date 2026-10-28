import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from passlib.hash import pbkdf2_sha256 as sha256
from jose import jwt
from passlib.context import CryptContext

# Set a real secret in your environment for anything beyond local testing:
#   $env:SECRET_KEY = "a-long-random-string"
SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-secret-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return sha256.verify(plain_password, hashed_password)


def get_password_hash(password):
    hash = sha256.hash(password)
    hash = str(hash)
    return hash


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
