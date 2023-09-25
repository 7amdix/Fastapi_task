from fastapi import FastAPI, HTTPException,Depends
from pydantic import BaseModel,EmailStr
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import Body
from sqlalchemy.orm import Session
from . import models,utils
from .database import engine, get_db
import json
import logging 

from .routers import user,task,auth
app = FastAPI()
models.Base.metadata.create_all(bind=engine)


    
    
try:
    conn=psycopg2.connect(host="localhost",database="To-do list",user='postgres',password="2012002a",cursor_factory=RealDictCursor)
    cursor =conn.cursor()
    print("done")
except Exception as error:
    print("conn failed")
    print("error",error)    
    
    
    
app.include_router(task.router)    
app.include_router(user.router)
app.include_router(auth.router)    
    

    
    
    
@app.get("/")
def root():
    return{"Message":"FastAPI Task"}
