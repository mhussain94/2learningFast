from datetime import datetime, timedelta
from jose import JWTError, jwt

#secret key created with "openssl rand -hex 32"
SECRET_KEY = "b116705ddd2dbd2f7461a6fba503dab791902bf50e3b14046c49768005cc230a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt