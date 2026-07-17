"""
MySQL CSV to Database Importer
==============================
This script automatically imports all CSV files from a specified folder into a MySQL database.
Each CSV file becomes a separate table named after the file.

Requirements:
    - pandas
    - sqlalchemy
    - pymysql

Usage:
    Update the USER CONFIGURATION SECTION below and run the script.
"""

import os
import time
import logging
import gc
import csv
from pathlib import Path
from typing import List, Tuple, Any

import pandas as pd
from sqlalchemy import create_engine, text, exc
from urllib.parse import quote_plus

# ==================================================
# USER CONFIGURATION SECTION
# ==================================================
HOST = "localhost"
PORT = 3306
USERNAME = "root"
PASSWORD = "Pajju@2005"             # Update with your correct MySQL password
DATABASE_NAME = "my_database"
CSV_FOLDER = "./csv_files"        # Folder containing CSV files
CHUNK_SIZE = 50000                # Number of rows to process at a time
POOL_SIZE = 5
MAX_OVERFLOW = 10
LOG_FILE = "import_mysql.log"     # Log file name
ECHO_SQL = False                  # Set to True to print SQL queries (debugging)
# ==================================================

# Console colors for professional logging output (Bonus Feature)
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


# Set up logging for error and audit trailing
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def validate_folder(folder_path: str) -> Path:
    """Validates that the folder exists and returns a Path object."""
    path = Path(folder_path)
    if not path.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")
    if not path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {folder_path}")
    return path


def find_csv_files(folder_path: Path) -> List[Path]:
    """Finds all visible CSV files in the given folder, ignoring hidden and non-csv files."""
    csv_files = []
    for file in folder_path.iterdir():
        if file.is_file() and file.suffix.lower() == ".csv" and not file.name.startswith("."):
            csv_files.append(file)
    return sorted(csv_files)


def detect_encoding(file_path: Path) -> str:
    """Attempts to intelligently detect the file encoding."""
    encodings = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252']
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                f.read(10000)
                return enc
        except UnicodeDecodeError:
            continue
    return 'utf-8'


def detect_delimiter(file_path: Path, encoding: str) -> str:
    """Attempts to intelligently detect the CSV delimiter."""
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            sample = f.read(10000)
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(sample)
            return dialect.delimiter
    except Exception:
        return ','  # Default to comma on failure


def create_mysql_server_engine() -> Any:
    """Creates a SQLAlchemy engine connected to the MySQL server (without a specific database)."""
    db_url = f"mysql+pymysql://{USERNAME}:{quote_plus(PASSWORD)}@{HOST}:{PORT}/"
    try:
        engine = create_engine(
            db_url,
            pool_size=POOL_SIZE,
            max_overflow=MAX_OVERFLOW,
            echo=ECHO_SQL
        )
        # Test connection
        with engine.connect() as conn:
            pass
        return engine
    except Exception as e:
        logger.error(f"Failed to connect to MySQL server: {e}")
        raise


def create_database_if_not_exists(server_engine: Any, database_name: str) -> None:
    """Creates the target database if it does not already exist."""
    try:
        with server_engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{database_name}`"))
            logger.info(f"Verified/Created database: {database_name}")
    except Exception as e:
        logger.error(f"Failed to create database '{database_name}': {e}")
        raise


def create_mysql_engine(database_name: str) -> Any:
    """Creates and returns a SQLAlchemy MySQL engine for the specific target database."""
    db_url = f"mysql+pymysql://{USERNAME}:{quote_plus(PASSWORD)}@{HOST}:{PORT}/{database_name}"
    try:
        engine = create_engine(
            db_url,
            pool_size=POOL_SIZE,
            max_overflow=MAX_OVERFLOW,
            echo=ECHO_SQL
        )
        # Test connection
        with engine.connect() as conn:
            pass
        return engine
    except Exception as e:
        logger.error(f"Failed to connect to MySQL database '{database_name}': {e}")
        raise


def import_csv(file_path: Path, engine: Any, chunk_size: int) -> Tuple[bool, int, str]:
    """
    Imports a single CSV file into the database.
    Returns a tuple of (success_status, rows_imported, error_message).
    """
    table_name = file_path.stem
    rows_imported = 0
    
    try:
        encoding = detect_encoding(file_path)
        delimiter = detect_delimiter(file_path, encoding)
        
        # Read and insert in chunks to save memory
        first_chunk = True
        for chunk in pd.read_csv(
            file_path,
            chunksize=chunk_size,
            encoding=encoding,
            delimiter=delimiter,
            low_memory=False
        ):
            # First chunk replaces any existing table, subsequent chunks append 
            if_exists_action = "replace" if first_chunk else "append"
            
            # Using chunk.to_sql handles transaction commit automatically 
            chunk.to_sql(
                name=table_name,
                con=engine,
                if_exists=if_exists_action,
                index=False
            )
            rows_imported += len(chunk)
            first_chunk = False
            
            # Explicit garbage collection for optimal memory efficiency
            del chunk
            gc.collect()
            
        return True, rows_imported, ""
    except exc.SQLAlchemyError as e:
        return False, rows_imported, f"Database Error: {str(e)}"
    except UnicodeDecodeError as e:
        return False, rows_imported, f"Encoding Error: {str(e)}"
    except pd.errors.EmptyDataError:
        return False, rows_imported, "File is empty"
    except Exception as e:
        return False, rows_imported, f"Unexpected Error: {str(e)}"


def import_all_csvs() -> Tuple[int, int, int, float]:
    """
    Orchestrates folder validation, database creation, and batch importing of all CSVs.
    Returns (total_files, succeeded, failed, total_time).
    """
    start_time = time.time()
    
    try:
        folder = validate_folder(CSV_FOLDER)
    except Exception as e:
        print(f"{Colors.FAIL}Initialization Failed: {e}{Colors.ENDC}")
        logger.error(f"Initialization Failed: {e}")
        return 0, 0, 0, 0.0
        
    print(f"Scanning folder...")
    csv_files = find_csv_files(folder)
    total_files = len(csv_files)
    
    if total_files == 0:
        print(f"{Colors.WARNING}No CSV files found in '{CSV_FOLDER}'.{Colors.ENDC}")
        return 0, 0, 0, 0.0
        
    print(f"Found {total_files} CSV files\n")
    print("-" * 50)
    
    try:
        # Step 1: Connect to MySQL server and automatically create DB if missing
        server_engine = create_mysql_server_engine()
        create_database_if_not_exists(server_engine, DATABASE_NAME)
        server_engine.dispose()
        
        # Step 2: Connect to the specific database for table creation and data import
        engine = create_mysql_engine(DATABASE_NAME)
    except Exception:
        print(f"{Colors.FAIL}Fatal Error: Could not establish a database connection. Exiting.{Colors.ENDC}")
        return total_files, 0, 0, 0.0
        
    succeeded = 0
    failed = 0
    
    for i, file_path in enumerate(csv_files, 1):
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        print(f"[{i}/{total_files}]")
        print(f"{file_path.name}")
        print("Table:")
        print(f"{file_path.stem}")
        
        file_start_time = time.time()
        success, rows, error_msg = import_csv(file_path, engine, CHUNK_SIZE)
        file_time = time.time() - file_start_time
        
        print("Rows Imported:")
        print(f"{rows:,}")
        
        if success:
            print("Status:")
            print(f"{Colors.OKGREEN}SUCCESS{Colors.ENDC}")
            print("Time:")
            print(f"{file_time:.2f} sec")
            succeeded += 1
            logger.info(f"Successfully imported {file_path.name} ({rows} rows) in {file_time:.2f}s")
        else:
            print("Status:")
            print(f"{Colors.FAIL}FAILED{Colors.ENDC}")
            print("Reason:")
            print(f"{error_msg}")
            print("Continuing...")
            failed += 1
            logger.error(f"Failed to import {file_path.name}: {error_msg}")
            
        print("-" * 50)
            
    # Dispose the engine connection pool cleanly
    engine.dispose()
    
    total_time = time.time() - start_time
    return total_files, succeeded, failed, total_time


def print_summary(total_files: int, succeeded: int, failed: int, total_time: float) -> None:
    """Prints a professional summary of the import process."""
    print("IMPORT COMPLETED")
    print("Processed:")
    print(f"{total_files}")
    print("Succeeded:")
    print(f"{Colors.OKGREEN}{succeeded}{Colors.ENDC}")
    print("Failed:")
    if failed > 0:
        print(f"{Colors.FAIL}{failed}{Colors.ENDC}")
    else:
        print(f"{failed}")
    print("=" * 50)


def main() -> None:
    """Main entry point for the script."""
    print("=" * 50)
    print(f"{Colors.BOLD}CSV TO MYSQL IMPORTER{Colors.ENDC}")
    print("=" * 50)
    
    total_files, succeeded, failed, total_time = import_all_csvs()
    
    if total_files > 0:
        print_summary(total_files, succeeded, failed, total_time)


if __name__ == "__main__":
    main()
