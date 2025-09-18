import jwt
import os
from jwt.exceptions import InvalidTokenError
from datetime import datetime, UTC, timedelta

def create_access_token(data: dict):
    SECRET_KEY=os.getenv("SECRET_KEY")
    ALGORITHM=os.getenv("ALGORITHM")

    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(hours=2)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

