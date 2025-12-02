import logging

import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from db.database import SessionDB
from utils.schemas import TABLES_MAP


def transform_date(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert date string columns to pandas datetime objects.

    Converts common datetime columns (birth_date, created_at, sent_at) from
    string format to pandas Timestamp objects for database insertion.
    Handles parsing errors gracefully without raising exceptions.

    Args:
        df: DataFrame containing date columns as strings

    Returns:
        DataFrame with date columns converted to datetime type
    """
    COLUMNS_DATETIME = ["birth_date", "created_at", "sent_at"]
    for col in COLUMNS_DATETIME:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
    return df


def save_dataframe_to_table(session: Session, df: pd.DataFrame, model):
    """
    Insert dataframe rows into a database table via bulk insert.

    Converts dataframe to list of dictionaries matching the model schema,
    transforms date columns to datetime objects, and performs bulk insert.
    Logs warning if dataframe is empty.

    Args:
        session: SQLAlchemy Session object for database operations
        df: DataFrame rows to insert
        model: SQLAlchemy ORM model class corresponding to target table

    Returns:
        Empty string on success

    Raises:
        SQLAlchemyError: If database insertion fails (caught and re-raised with logging)
    """
    if df.empty or df is None:
        logging.warning(f"There is no data to save for table {model.__tablename__}")
        return

    df = transform_date(df)
    records_table = df.to_dict(orient="records")

    try:
        session.bulk_insert_mappings(model, records_table)
        return ""
    except SQLAlchemyError as e:
        logging.error(f"Error saving data to table {model.__tablename__}: {e}")
        raise


def save_data(data: dict[str, pd.DataFrame]):
    """
    Save validated dataframes to the database in a single transaction.

    Iterates through all table mappings (from TABLES_MAP), inserts each dataframe
    into its corresponding table via save_dataframe_to_table(). If any error occurs,
    rolls back all changes to maintain data consistency.

    Args:
        data: Dictionary mapping table names to validated pandas DataFrames

    Raises:
        Exception: On transaction failure (after rollback and logging)
    """
    session: Session = SessionDB()

    try:
        for table_name, model in TABLES_MAP.items():
            save_dataframe_to_table(session, data.get(table_name), model)

        session.commit()
        logging.info("All clean data saved successfully to the database")
    except Exception as e:
        session.rollback()
        logging.error(f"Error saving data, rolled back transaction: {e}")
        raise

    session.close()
