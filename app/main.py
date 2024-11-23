from fastapi import FastAPI

from .database import Base, engine
from .routers import customers

# Initialize database
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="FastAPI Customer Management API",
    description="API for managing customers",
    version="1.0.0",
    contact={
        "name": "Jay",
        "email": "jaijayanth@gmail.com",
    },
)

# Include routers
app.include_router(customers.router)
