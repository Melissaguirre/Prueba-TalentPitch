import logging

from sqlalchemy import event, create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base


URL_DATABASE = "sqlite:///talentpitch_data_clean.db"
engine = create_engine(URL_DATABASE, echo=False, future=True)


@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    """
    Enable SQLite foreign key constraints on each new connection.

    SQLite disables foreign keys by default. This listener ensures they are
    activated for all database connections to maintain referential integrity.

    Args:
        dbapi_connection: Raw DBAPI connection object
        connection_record: SQLAlchemy connection record metadata
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()


SessionDB = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def init_db():
    """
    Initialize the database schema and create all tables.

    Creates all tables defined in Base.metadata based on SQLAlchemy ORM models.
    Foreign key constraints are enabled via the 'enable_foreign_keys' event listener.

    Returns:
        Engine: SQLAlchemy engine instance for database operations
    """
    Base.metadata.create_all(bind=engine)
    logging.info("Database successfully initialized")
    return engine
