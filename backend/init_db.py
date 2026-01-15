"""Script to initialize database tables."""
from sqlmodel import SQLModel
from db import engine
from models import Task, User  # Import all models that need tables created


def create_tables():
    """Create all database tables."""
    print("Creating database tables...")
    SQLModel.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    create_tables()