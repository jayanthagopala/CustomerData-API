from fastapi import FastAPI

from .database import Base, engine
from .routers import customers

# Initialize database
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()

# Include routers
app.include_router(customers.router, prefix="/customers", tags=["customers"])
