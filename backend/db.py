from sqlmodel import create_engine, Session
from typing import Generator
import os

# Get database URL from environment, with a default for testing
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_test.db")

# Create the database engine
engine = create_engine(DATABASE_URL, echo=False)


def get_session() -> Generator[Session, None, None]:
    """Dependency to get a database session."""
    with Session(engine) as session:
        yield session