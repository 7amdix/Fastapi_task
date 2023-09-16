from fastapi import FastAPI, HTTPException,Depends
from pydantic import BaseModel,EmailStr
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import Body
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
import json

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class Userss(BaseModel):
    email=EmailStr
    password=str
class TodoItem(BaseModel):
    name: str
    description: str
    
    
try:
    conn=psycopg2.connect(host="localhost",database="To-do list",user='postgres',password="2012002a",cursor_factory=RealDictCursor)
    cursor =conn.cursor()
    print("done")
except Exception as error:
    print("conn failed")
    print("error",error)    
@app.get("/")
def root():
    return{"Message":"FastAPI Task"}

# @app.post("/users")
# def create_user(userr:Userss, db: Session=Depends(get_db)):
#     new_user=models.User(**userr.dict())
#     # json.dumps(new_user)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return{"data": new_user}

@app.post("/users")
def create_users(User: Userss, db: Session=Depends(get_db)):
    # cursor.execute(""" insert into "Tasks" (name,description) values (%s,%s) returning * """,(Task.name,Task.description))
    # new_task=cursor.fetchone()
    # conn.commit()
    new_user=models.UserModel(**User.dict())
    db  .add(new_user)
    db.commit()
    db.refresh(new_user)
    return{"data": new_user}

@app.get("/Tasks")
def get_tasks(db: Session=Depends(get_db)):
    # cursor.execute(""" SELECT * FROM "Tasks" """)
    # Tasks=cursor.fetchall()
    Tasks=db.query(models.TodoItem).all()
    print (Tasks)
    return{"data":Tasks}
    
 
@app.get("/Tasks/{id}")  
def get_post(id: int, db: Session=Depends(get_db)):
    # cursor.execute(""" Select * from "Tasks" where "id" = %s """,(str(id)))
    # Specific_task=cursor.fetchone()
    Specific_task=db.query(models.TodoItem).filter(models.TodoItem.id==id).first()
    return{"Specific_Task": Specific_task}        

@app.post("/Tasks")
def create_tasks(Task: TodoItem, db: Session=Depends(get_db)):
    # cursor.execute(""" insert into "Tasks" (name,description) values (%s,%s) returning * """,(Task.name,Task.description))
    # new_task=cursor.fetchone()
    # conn.commit()
    new_task=models.TodoItem(**Task.dict())
    db  .add(new_task)
    db.commit()
    db.refresh(new_task)
    return{"data": new_task}


@app.delete("/Tasks/{id}")    
def delete_Tasks(id: int,db: Session=Depends(get_db)):
    # cursor.execute(""" DELETE from "Tasks" where "id"= %s returning * """,(str (id)),)
    # deleted_task=cursor.fetchone()
    # conn.commit()
    specific_task_delete=db.query(models.TodoItem).filter(models.TodoItem.id==id)
    specific_task_delete.delete(synchronize_session=False)
    db.commit()
    return{"Message":"Task deleted successfully"}

@app.put("/Tasks/{id}")
def update_Task(id: int, Task:TodoItem,db: Session=Depends(get_db)):
    # cursor.execute("""Update "Tasks" set "name" = %s, "description" = %s where id=%s returning * """,(Task.name,Task.description,str(id)))
    # updated_post=cursor.fetchone()
    # conn.commit()
    update_Specific_task=db.query(models.TodoItem).filter(models.TodoItem.id==id)
    update_Specific_task.update(Task.dict(),synchronize_session=False)
    db.commit
    return{"data":  update_Specific_task.first()}


    