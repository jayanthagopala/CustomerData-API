import os

from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base, sessionmaker

from app.utils.logger import setup_logger

# Load environment variables from .env file
load_dotenv()

# Get the database URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./customers.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

crud_logger = setup_logger("crud-operations", "crud.log")


def get_db():
    try:
        db = SessionLocal()
        yield db
    except OperationalError as e:
        crud_logger.error(f"Database connection failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Database connection failed. Please try again later.",
        )
    finally:
        db.close()
