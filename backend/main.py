from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import tasks
from routes import auth
from config import settings
from sqlmodel import SQLModel
from db import engine
from models import Task  # Import models to register them with SQLModel


# Create database tables on startup
def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)


# Create FastAPI app with API versioning
app = FastAPI(
    title="Todo Backend API",
    version="1.0.0",
    description="Secure Todo API with JWT authentication and user isolation"
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "Authorization"],  # Include Authorization header for JWT
)


# Include the auth and tasks routers
app.include_router(auth.router, prefix="/api")
app.include_router(tasks.router, prefix="/api/v1")


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["."]
    )