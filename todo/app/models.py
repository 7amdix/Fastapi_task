from sqlalchemy import Column,Integer,String,Boolean
from sqlalchemy.sql.expression import null
from .database import Base

class TodoItem(Base):
    __tablename__="Taskss"
    id= Column(Integer,primary_key=True,nullable=False)
    name= Column(String,nullable=False)
    description= Column(String, nullable=False)
    
class UserModel(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False, unique=True)
    password=Column(String,nullable=False)        