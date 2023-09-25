from .. import utils,models,oauth2
from fastapi import FastAPI, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import database
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from pydantic import BaseModel,EmailStr

router= APIRouter(tags=["Authentication"])

class UserLogin(BaseModel):
    email:EmailStr
    password:str
    

@router.post("/login")
def login(user_credentials :OAuth2PasswordRequestForm=Depends(), db: Session=Depends(database.get_db)):
  user = db.query(models.UserModel).filter(models.UserModel.email == user_credentials.username).first()
  utils.verify(user_credentials.password,user.password)
  access_token=oauth2.create_acces_token(data={"user_id": user.id })
  return{"access_token" : access_token,"token_type":"bearer"}
      
 