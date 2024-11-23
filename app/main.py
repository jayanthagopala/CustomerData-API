import logging

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .database import Base, engine
from .routers import customers

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Request validation failed. Ensure all required fields are included.",
            "errors": exc.errors(),
        },
    )


# Include routers
app.include_router(customers.router)
