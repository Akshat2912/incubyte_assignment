from sqlmodel import SQLModel, create_engine, Session
from pathlib import Path
DB_URL = "sqlite:///./sweetshop.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

def init_db():
    SQLModel.metadata.create_all(engine)
