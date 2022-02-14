from base64 import encode
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "1a9e4b835f98e902d0d8cb5006e61efed716b95451533b8b1a43140beea272e9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
