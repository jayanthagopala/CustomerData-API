import os

from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base, sessionmaker

from app.utils.logger import setup_logger

# Load environment variables from .env file
load_dotenv()

"""
The database URL is loaded from an environment variable, or a default
SQLite database file is used if the environment variable is not set.
"""

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./customers.db")

"""
Create a SQLAlchemy engine using the database URL. The
`check_same_thread` argument is set to False to allow the SQLite
database to be used in a multi-threaded environment.
"""
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

"""
Create a session maker factory that will produce database sessions.
The sessions are configured to be non-autocommitting and non-autoflush,
and are bound to the engine created earlier.
"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

"""
Create a declarative base class that will be used to define database models.
This base class provides the necessary functionality for SQLAlchemy to
map Python classes to database tables.
"""
Base = declarative_base()

"""
Set up a logger for CRUD (Create, Read, Update, Delete) operations.
This logger will be used to log errors and other relevant information
related to database interactions.
"""
crud_logger = setup_logger("crud-operations", "crud.log")


def get_db():
    """
    This function provides a context manager for getting a database session.
    It sets up the session, yields it to the caller, and automatically
    closes the session when the context is exited.
    """
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
