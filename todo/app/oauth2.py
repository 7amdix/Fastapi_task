from jose import JWTError, jwt
from datetime import datetime,timedelta
from pydantic import BaseModel,EmailStr
from typing import Optional
from fastapi import Depends,status
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme= OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str
    
class Token_Data(BaseModel):
    id: Optional[str]=None


def create_acces_token(data: dict):
   encoded_data= data.copy()
   expire= datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
   encoded_data.update({"exp":expire})
   encoded_jwt=jwt.encode(encoded_data,SECRET_KEY,algorithm=ALGORITHM)
   return encoded_jwt
   
def verify_access_token(token: str):
    payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    id :str =payload.get("user_id")
    TokenData=Token_Data(id=id)
    return TokenData
    
def get_current_user(token: str=Depends(oauth2_scheme)):
    return verify_access_token(token)
   
   
