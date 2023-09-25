from .. import utils,models,oauth2
from fastapi import FastAPI, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db
from pydantic import BaseModel,EmailStr






router=APIRouter(
    prefix="/Tasks",
    tags=['Tasks']
)



class TodoItem(BaseModel):
    name:str
    description: str




@router.get("/")
def get_tasks(db: Session=Depends(get_db)):
    # cursor.execute(""" SELECT * FROM "Tasks" """)
    # Tasks=cursor.fetchall()
    Tasks=db.query(models.TodoItem).all()
    print (Tasks)
    return{"data":Tasks}
    
 
@router.get("/{id}")  
def get_post(id: int, db: Session=Depends(get_db)):
    # cursor.execute(""" Select * from "Tasks" where "id" = %s """,(str(id)))
    # Specific_task=cursor.fetchone()
    Specific_task=db.query(models.TodoItem).filter(models.TodoItem.id==id).first()
    return{"Specific_Task": Specific_task}        

@router.post("/")
def create_tasks(Task: TodoItem, db: Session=Depends(get_db), get_current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" insert into "Tasks" (name,description) values (%s,%s) returning * """,(Task.name,Task.description))
    # new_task=cursor.fetchone()
    # conn.commit()
    new_task=models.TodoItem(**Task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return{"data": new_task}


@router.delete("/{id}")    
def delete_Tasks(id: int,db: Session=Depends(get_db)):
    # cursor.execute(""" DELETE from "Tasks" where "id"= %s returning * """,(str (id)),)
    # deleted_task=cursor.fetchone()
    # conn.commit()
    specific_task_delete=db.query(models.TodoItem).filter(models.TodoItem.id==id)
    specific_task_delete.delete(synchronize_session=False)
    db.commit()
    return{"Message":"Task deleted successfully"}

@router.put("/{id}")
def update_Task(id: int, Task:TodoItem,db: Session=Depends(get_db)):
    # cursor.execute("""Update "Tasks" set "name" = %s, "description" = %s where id=%s returning * """,(Task.name,Task.description,str(id)))
    # updated_post=cursor.fetchone()
    # conn.commit()
    update_Specific_task=db.query(models.TodoItem).filter(models.TodoItem.id==id)
    update_Specific_task.update(Task.dict(),synchronize_session=False)
    db.commit
    return{"data":  update_Specific_task.first()}