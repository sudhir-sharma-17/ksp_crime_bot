import os
import logging
import zcatalyst_sdk
from sqlalchemy import create_engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Catalyst app (wrapped in try-except to prevent startup crash in local dev environments)
catalyst_app = None
datastore = None

try:
    catalyst_app = zcatalyst_sdk.initialize()
    datastore = catalyst_app.datastore()
except Exception as e:
    logger.warning(f"Catalyst SDK initialization failed ({e}). Proceeding in offline development mode.")

class CatalystRow:
    def __init__(self, mapping):
        self._mapping = mapping

class CatalystResult:
    def __init__(self, rows):
        self.returns_rows = True
        self._rows = [CatalystRow(r) for r in rows]

    def fetchall(self):
        return self._rows

class CatalystConnection:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def execute(self, statement, *args, **kwargs):
        # Convert statement to string SQL
        sql_str = str(statement)
        logger.info(f"Executing ZCQL via Catalyst: {sql_str}")
        
        try:
            if catalyst_app is None:
                raise ValueError("Catalyst SDK not initialized")
            # Query example using Zoho's ZCQL (Zoho Catalyst Query Language)
            zcql_result = catalyst_app.zcql().execute_query(sql_str)
            # Catalyst returns list of dicts, flatten for SQLAlchemy row_mapping compatibility
            flattened_rows = []
            for row in zcql_result:
                flat_row = {}
                for val in row.values():
                    if isinstance(val, dict):
                        flat_row.update(val)
                flattened_rows.append(flat_row)
            return CatalystResult(flattened_rows)
        except Exception as e:
            logger.warning(f"Catalyst ZCQL failed ({e}). Falling back to local MySQL/SQLAlchemy for offline presentation.")
            # Fallback to standard MySQL connection so development/presentation works 100% offline
            db_user = os.environ.get("DB_USER", "root")
            db_password = os.environ.get("DB_PASSWORD", "")
            db_host = os.environ.get("DB_HOST", "localhost")
            db_port = os.environ.get("DB_PORT", "3306")
            db_name = os.environ.get("DB_NAME", "KarnatakaPoliceFIRDB")
            encoded_password = db_password.replace("@", "%40")
            database_url = f"mysql+pymysql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"
            
            engine = create_engine(database_url, pool_pre_ping=True, pool_recycle=3600)
            with engine.connect() as conn:
                res = conn.execute(statement, *args, **kwargs)
                if res.returns_rows:
                    return CatalystResult([dict(r._mapping) for r in res.fetchall()])
                return CatalystResult([])

class CatalystEngine:
    def connect(self):
        return CatalystConnection()

def get_db_connection():
    """
    Returns the Catalyst database adapter wrapping Zoho Catalyst SDK ZCQL
    with a local SQLAlchemy MySQL fallback for reliable offline presentation.
    """
    return CatalystEngine()
