import pandas as pd
import logging
from pathlib import Path
from utils.schemas import FIELDS_FILES
from utils.validators import complete_validations


def read_file(file_path: Path) -> pd.DataFrame:
    """
    Read a CSV file and return as a pandas DataFrame.

    Handles read errors gracefully by logging errors and returning
    an empty DataFrame instead of raising exceptions.

    Args:
        file_path: Path object pointing to the CSV file

    Returns:
        DataFrame with CSV contents; empty DataFrame if read fails
    """
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        logging.error(f"Error reading {file_path}: {e}")
        return pd.DataFrame()


def load_data() -> dict:
    """
    Load and validate CSV data files from the data directory. 

    Process flow: 
    1. Load each CSV file from the data directory from FIELDS_FILES schema
    2. Apply complete validation rules to each dataframe 
    3. Store a dictionary of validated dataframes by file name
    
    Returns: 
        dict: Dictionary mapping file names to validated pandas DataFrames
    """
    logging.info("Loading data from CSV files")
    data_dir = Path("data")
    data = {}

    for name_file, fields in FIELDS_FILES.items():
        logging.info(f"Loading {name_file}")

        file_path = data_dir / f"{name_file}.csv"
        if file_path.exists():
            df_file = read_file(file_path)
            logging.info(f"File {name_file} loaded with {df_file.shape[0]} records")

            data[name_file] = df_file
            df_file_with_validations = complete_validations(
                df_file, name_file, data, fields
            )
            data[name_file] = df_file_with_validations
        else:
            logging.warning(f"File {name_file} not found")

    return data
