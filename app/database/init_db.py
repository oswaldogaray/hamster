from app.database.database import create_db_and_tables


def initialize_database() -> None:
    """Initialize database schema for local development and first run."""
    create_db_and_tables()
