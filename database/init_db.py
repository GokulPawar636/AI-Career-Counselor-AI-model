from database.db import engine
from database.models import Base

def init_database():
    """
    Create all database tables if they don't exist.
    Safe to call every time the application starts.
    """
    Base.metadata.create_all(bind=engine)


# Optional alias for backward compatibility
def init_db():
    init_database()
