import os
import logging
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load local environment variables if present
load_dotenv()

# Configure logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    """
    Returns a standard SQLAlchemy engine connected to the Railway MySQL instance
    using credentials from environment variables.
    """
    db_user = os.getenv("DB_USER", "root").strip()
    db_password = os.getenv("DB_PASSWORD", "").strip()
    db_host = os.getenv("DB_HOST", "localhost").strip()
    db_port = os.getenv("DB_PORT", "3306").strip()
    db_name = os.getenv("DB_NAME", "KarnatakaPoliceFIRDB").strip()
    
    # Safely encode the password for the connection URL
    encoded_password = quote_plus(db_password)
    database_url = f"mysql+pymysql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"
    
    return create_engine(
        database_url,
        pool_pre_ping=True,
        pool_recycle=3600
    )

