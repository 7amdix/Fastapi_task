from .. import utils,models
from fastapi import FastAPI, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db
from pydantic import BaseModel,EmailStr

router=APIRouter(
    prefix="/users",
    tags=['Users']
)

class Userss(BaseModel):
    email:EmailStr
    password:str


# @app.post("/users")
# def create_user(userr:Userss, db: Session=Depends(get_db)):
#     new_user=models.User(**userr.dict())
#     # json.dumps(new_user)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return{"data": new_user}

@router.post("/")
def create_users(User: Userss, db: Session=Depends(get_db)):
    # cursor.execute(""" insert into "Tasks" (name,description) values (%s,%s) returning * """,(Task.name,Task.description))
    # new_task=cursor.fetchone()
    # conn.commit()
    Hashed_password=utils.hash(User.password)
    User.password=Hashed_password
    new_user=models.UserModel(**User.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return{"data": new_user}




@router.get("/{id}")
def get_user_task(id: int,db: Session=Depends(get_db)):
   get_user=db.query(models.UserModel).filter(models.UserModel.id == id).first()
   return get_user
    