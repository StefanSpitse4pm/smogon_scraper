from settings import DB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DB.DB_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
