from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from typing import Annotated
from config import settings
from jose import JWTError, jwt
from data.crud_db import get_user

# Использование настроек
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

router = APIRouter(prefix="/login")

@router.post("/")
async def login(data:OAuth2PasswordRequestForm = Depends()) :
    user = await get_user(data.username)
    if not user or user["password"] != data.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    else:
        return {"access_token": create_access_token(user), "token_type": "bearer"}
   

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
def create_access_token(data: dict, expires_delta: timedelta | None = None):    
    to_encode = data.copy()    
    if expires_delta:        
        expire = datetime.now(timezone.utc) + expires_delta    
    else:        
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)    
    to_encode.update({"exp": expire})    
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)    
    return encoded_jwt

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):    
    try:        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")  
        print(username)       
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")        
        user = username 

        if user is None:            
            raise HTTPException(status_code=401, detail="Tasks not found")        
        return user    
    except JWTError:        
        raise HTTPException(status_code=401, detail="Could not validate credentials")