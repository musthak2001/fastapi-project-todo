from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

# Option 1: get from .env file
DATABASE_URL = os.getenv("DATABASE_URL")


# DATABASE_URL = "postgresql://postgres:test1234@localhost:5432/todo_DB"

# Create engine
engine = create_engine(DATABASE_URL)

# Create SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
