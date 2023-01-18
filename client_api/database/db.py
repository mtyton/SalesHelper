from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from api import settings


def build_database_url() -> str:
    return f"postgresql://{settings.POSTGRES_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.POSTGRES_DB}"


engine = create_engine(
    build_database_url()
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
