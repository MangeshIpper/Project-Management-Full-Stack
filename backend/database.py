from sqlalchemy import create_engine
from security.config import settings
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_engine(settings.database_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()