from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

DATABASE_URL = settings.database_url
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set in the environment variable")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind = engine,
    autoflush = False
)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()