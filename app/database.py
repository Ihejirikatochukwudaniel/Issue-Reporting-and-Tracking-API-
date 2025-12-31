from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DATABASE_URL: Connection string for our database
# "sqlite:///./issues.db" means:
#   - sqlite:// → We're using SQLite database
#   - ./ → Current directory
#   - issues.db → Database file name
DATABASE_URL = "sqlite:///./issues.db"

# create_engine: Creates the database engine (connection manager)
# check_same_thread=False: Required for SQLite to work with FastAPI
# (allows multiple threads to use the same connection)
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# SessionLocal: Factory for creating database sessions
# A session is like a "workspace" for database operations
# autocommit=False: We control when to save changes (more control)
# autoflush=False: We control when to sync with database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: Base class for all our database models (tables)
# All table definitions will inherit from this
Base = declarative_base()


def get_db():
    """
    Dependency function that provides database sessions to our routes.
    
    This is a "generator function" (notice the 'yield' keyword).
    It creates a new database session for each request and automatically
    closes it when the request is done, even if an error occurs.
    
    Why use this pattern?
    - Ensures we don't leave database connections open
    - Each request gets its own isolated session
    - Automatic cleanup prevents memory leaks
    """
    db = SessionLocal()
    try:
        yield db  # Give the session to whoever needs it
    finally:
        db.close()  # Always close when done