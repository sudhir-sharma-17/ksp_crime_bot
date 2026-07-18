import os
import sys
import gc
import csv
from pathlib import Path
import mysql.connector
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# Ensure required libraries are installed
try:
    import pandas as pd
    from dotenv import load_dotenv
except ImportError:
    print("[ERROR] Critical dependencies missing. Please install them first:")
    print("   pip install pandas python-dotenv mysql-connector-python sqlalchemy pymysql")
    sys.exit(1)

# Locate directories relative to this setup script
BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR / "backend"
ENV_PATH = BACKEND_DIR / ".env"
ENV_EXAMPLE_PATH = BACKEND_DIR / ".env.example"
CSV_FOLDER = BASE_DIR / "csv_files"

# Load environment variables
load_dotenv(dotenv_path=ENV_PATH)

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_NAME = os.environ.get("DB_NAME", "KarnatakaPoliceFIRDB")
DB_PORT = int(os.environ.get("DB_PORT", "3306"))

print("=" * 60)
print("STARTING DATABASE SETUP WITH EXACT CSV DATA ONLY")
print(f"   Database: {DB_NAME}")
print(f"   Host:     {DB_HOST}:{DB_PORT}")
print(f"   User:     {DB_USER}")
print("=" * 60)

# Helper functions for CSV detection
def detect_encoding(file_path: Path) -> str:
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
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            sample = f.read(10000)
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(sample)
            return dialect.delimiter
    except Exception:
        return ','

# Connect and create database
try:
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`")
    conn.commit()
    cursor.close()
    conn.close()
    print(f"[INFO] Verified/Created database: {DB_NAME}")
except Exception as e:
    print(f"[ERROR] Failed to connect to MySQL server / create database: {e}")
    sys.exit(1)

# Create sqlalchemy engine
encoded_password = quote_plus(DB_PASSWORD)
database_url = f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(database_url, pool_recycle=3600)

# 2. Import CSV Files (Exact Data)
if CSV_FOLDER.exists() and CSV_FOLDER.is_dir():
    print("\n[INFO] Importing CSV files into database tables...")
    csv_files = sorted([f for f in CSV_FOLDER.iterdir() if f.is_file() and f.suffix.lower() == ".csv"])
    
    # Disable foreign key checks for dropping/creating tables cleanly
    try:
        with engine.connect() as conn:
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
            conn.commit()
    except Exception as e:
        print(f"Warning: could not disable FK checks: {e}")
        
    for i, file_path in enumerate(csv_files, 1):
        table_name = file_path.stem
        print(f"   [{i}/{len(csv_files)}] Importing {file_path.name} -> Table: {table_name}...", end="", flush=True)
        
        try:
            encoding = detect_encoding(file_path)
            delimiter = detect_delimiter(file_path, encoding)
            
            first_chunk = True
            rows_imported = 0
            for chunk in pd.read_csv(file_path, chunksize=10000, encoding=encoding, delimiter=delimiter, low_memory=False):
                if_exists_action = "replace" if first_chunk else "append"
                chunk.to_sql(name=table_name, con=engine, if_exists=if_exists_action, index=False)
                rows_imported += len(chunk)
                first_chunk = False
                del chunk
                gc.collect()
            print(f" Done ({rows_imported:,} rows)")
        except Exception as e:
            print(f" FAILED: {e}")
            
    # Re-enable foreign key checks
    try:
        with engine.connect() as conn:
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
            conn.commit()
    except Exception as e:
        print(f"Warning: could not re-enable FK checks: {e}")
else:
    print(f"[WARNING] CSV folder not found at {CSV_FOLDER}. Skipping CSV imports.")

# 3. Create Additional System Tables
print("\n[INFO] Creating required system tables (sessions, audit_logs, users)...")
try:
    with engine.connect() as conn:
        # Sessions
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id VARCHAR(255) PRIMARY KEY,
            user_id VARCHAR(255),
            data TEXT,
            expiry DATETIME
        );
        """))
        
        # Audit Logs
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_id VARCHAR(255),
            action VARCHAR(255),
            details TEXT
        );
        """))
        
        # Users
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE,
            password_hash VARCHAR(255),
            role VARCHAR(50)
        );
        """))
        conn.commit()
    print("[INFO] System tables set up successfully.")
except Exception as e:
    print(f"[ERROR] Failed to setup system tables: {e}")

print("\n" + "=" * 60)
print("DATABASE SETUP COMPLETE (EXACT DATA ONLY)!")
print("=" * 60)
