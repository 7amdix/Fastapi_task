from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sqlalchemy_database_url="postgresql://postgres:2012002a@localhost/To-do list"
engine=create_engine(sqlalchemy_database_url)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
