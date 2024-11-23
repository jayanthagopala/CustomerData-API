from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./customers.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    try:
        db = SessionLocal()
        yield db
    except OperationalError as e:
        raise HTTPException(
            status_code=500,
            detail="Database connection failed. Please try again later.",
        )
    finally:
        db.close()
