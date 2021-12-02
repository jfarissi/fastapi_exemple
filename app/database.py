import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
from .config import settings

SQL_DATABASE_ALCHEMY_URL =  f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"


engine = create_engine(SQL_DATABASE_ALCHEMY_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()


# while True:
# # Connect to your postgres DB
#     try:
#         conn = psycopg2.connect(host = 'localhost',database = 'fastapi',user='postgres',password = 'Oussama2006'
#         ,cursor_factory=RealDictCursor)
#         cur = conn.cursor()
#         print("connection was succesfull")
#         break    
#     # Open a cursor to perform database operations
#     # cur = conn.cursor()
#     except Exception as error:
#         print("connection failed!")
#         print("error!",error)
#         time.sleep(2)
        
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()