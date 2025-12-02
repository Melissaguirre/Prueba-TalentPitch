import logging
import pandas as pd

from utils.schemas import FIELDS_FK


def validation_emails_uniques(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate email entries from the dataframe.

    Identifies duplicate emails and keeps only the first occurrence.
    Logs warnings when duplicates are detected.

    Args:
        df: DataFrame containing user records with 'email' column (optional)

    Returns:
        DataFrame with duplicate emails removed; original if no 'email' column exists
    """

    logging.info("Validating unique emails")

    if "email" in df.columns:
        duplicates = df[df.duplicated(subset=["email"], keep=False)]
        if not duplicates.empty:
            logging.warning(f"emails duplicates found {duplicates['email'].unique()}")
        return df.drop_duplicates(subset=["email"])
    return df


def validation_required_fields(
    df: pd.DataFrame, required_fields: list[str]
) -> pd.DataFrame:
    """
    Remove rows with missing values in required fields.

    Args:
        df: DataFrame to validate
        required_fields: List of column names that must not be null

    Returns:
        DataFrame with rows containing missing required fields removed
    """
    logging.info("Validating required fields")

    missing_fields = df[df[required_fields].isnull().any(axis=1)]
    if not missing_fields.empty:
        logging.warning(
            f"{missing_fields.shape[0]} rows with missing required fields found"
        )
    return df.dropna(subset=required_fields)


def validation_valid_ids(df: pd.DataFrame, file_name: str) -> pd.DataFrame:
    """
    Validate and clean ID column in the dataframe.

    Performs four validation steps:
    1. Verify that 'id' column exists
    2. Remove records with null or empty IDs
    3. Sort by 'created_at' to preserve most recent duplicates
    4. Remove duplicate IDs, keeping the last (most recent) occurrence

    Logs detailed information about records removed at each step.

    Args:
        df: DataFrame to validate
        file_name: Source file name (used for logging context)

    Returns:
        DataFrame with validated and deduplicated IDs
    """

    if "id" not in df.columns:
        logging.warning(f"File {file_name} does not have 'id' column")
        return df

    logging.info(f"Validating IDs in file {file_name}")

    before_count = df.shape[0]
    df = df[df["id"].notnull() & (df["id"] != "")]
    removed_nulls = before_count - df.shape[0]
    if removed_nulls > 0:
        logging.warning(
            f"{removed_nulls} records with null or empty IDs removed in file {file_name}"
        )

    df = df.sort_values(by="created_at")
    before_duplicates = df.shape[0]
    df_depured = df.drop_duplicates(subset=["id"], keep="last").copy()
    df_depured["id"] = df_depured["id"].astype(int)
    removed_duplicates = before_duplicates - df_depured.shape[0]
    if removed_duplicates > 0:
        logging.warning(
            f"{removed_duplicates} duplicate IDs removed in file {file_name}"
        )

    logging.info(f"IDs successfully validated in in file {file_name}")

    return df_depured


def validation_foreign_keys(
    df: pd.DataFrame, file_name: str, data: dict[str, pd.DataFrame]
) -> pd.DataFrame:
    """
    Validate that all foreign key references exist in their source tables.

    Checks each FK field defined in FIELDS_FK in the referenced table.
    Removes rows with invalid FK values. 
    Logs warnings for missing columns and invalid references.

    Args:
        df: DataFrame to validate
        file_name: Source table name (must exist in FIELDS_FK to validate)
        data: Dictionary of all loaded DataFrames (for FK lookup)

    Returns:
        DataFrame with rows containing invalid FK values removed
    """

    if file_name not in FIELDS_FK:
        return df

    for fk_field, ref_table in FIELDS_FK[file_name].items():
        if fk_field not in df.columns:
            logging.warning(
                f"{file_name}: {fk_field} column does not exist in dataframe."
            )
            continue

        ref_key = "id" if "id" in data[ref_table].columns else "user_id"

        valid_values = data[ref_table][ref_key]
        before_count = df.shape[0]
        df = df[df[fk_field].isin(valid_values)]
        removed_count = before_count - df.shape[0]

        if removed_count > 0:
            logging.warning(
                f"{removed_count} records deleted in {file_name} for invalid FK {fk_field} - {ref_table}.{ref_key}"
            )

    return df


def complete_validations(
    df: pd.DataFrame,
    name_file: str,
    data: dict[str, pd.DataFrame],
    required_fields: list[str],
) -> pd.DataFrame:
    """
    Apply all validation rules to a dataframe.

    Validation order:
    1. Remove duplicate emails (if column exists)
    2. Remove rows with missing required fields
    3. Validate and deduplicate IDs
    4. Validate foreign key references against other tables

    Args:
        df: DataFrame to validate
        name_file: Name of the source file (used for logging and FK mapping)
        data: Dictionary of all loaded DataFrames (for FK validation)
        required_fields: List of columns that must not be null

    Returns:
        Fully validated DataFrame
    """
    final_df = validation_emails_uniques(df)
    final_df = validation_required_fields(final_df, required_fields)
    final_df = validation_valid_ids(final_df, name_file)
    final_df = validation_foreign_keys(final_df, name_file, data)
    return final_df
