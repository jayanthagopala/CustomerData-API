import logging
import time

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .database import Base, engine
from .routers import customers

# main.py
from .utils.logger import setup_logger

# Setup API logger
api_logger = setup_logger("fastapi-api", "api.log", level=logging.INFO)


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


# Add logging middleware to FastAPI app
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    api_logger.info(
        f"Method: {request.method} Path: {request.url.path} "
        f"Status: {response.status_code} Duration: {duration:.2f}s"
    )
    return response


# Include routers
app.include_router(customers.router)
