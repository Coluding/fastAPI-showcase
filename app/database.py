from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

SQL_URL = "postgresql://<username>:>password>@<ip-address/hostname>/<database_name>"

SQL_URL = "postgresql://postgres:Kripossi90!@localhost/fastapi" #Use env variables!!

engine = create_engine(SQL_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()