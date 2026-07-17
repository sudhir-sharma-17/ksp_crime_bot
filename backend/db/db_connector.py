import os
import logging
from db.database import get_db_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_engine():
    """Returns a validated database engine using Zoho Catalyst SDK adapter."""
    return get_db_connection()
