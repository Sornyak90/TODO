from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Annotated
from auth.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from jose import JWTError, jwt
from auth.fake_db import fake_users

router = APIRouter(prefix="/login")

@router.post("/")
def login(data:OAuth2PasswordRequestForm = Depends()) :
    user = fake_users.get(data.username)
    
    if not user or user["password"] != data.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    else:
        return {"access_token": create_access_token(user), "token_type": "bearer"}
   

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
def create_access_token(data: dict, expires_delta: timedelta | None = None):    
    to_encode = data.copy()    
    if expires_delta:        
        expire = datetime.utcnow() + expires_delta    
    else:        
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)    
    to_encode.update({"exp": expire})    
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)    
    return encoded_jwt

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):    
    try:        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")       
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")        
        user = username 

        if user is None:            
            raise HTTPException(status_code=401, detail="User not found")        
        return user    
    except JWTError:        
        raise HTTPException(status_code=401, detail="Could not validate credentials")