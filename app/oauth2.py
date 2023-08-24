from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta
from jose import jwt, JWTError

from . import schemas

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 0.5

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    jwt_encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_encoded

def verify_access_tocken(token : str, credentials_expection):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_expection
        token_data = schemas.TokenData(id=id)
    except JWTError:
        credentials_expection
    return token_data    
    
        

def get_current_users(token: str = Depends(oauth2_scheme)):
    credentials_expection= HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"could not validate credentials",
                                          headers={"WWW-Authenticate" : "bearer"})
    return verify_access_tocken(token, credentials_expection)