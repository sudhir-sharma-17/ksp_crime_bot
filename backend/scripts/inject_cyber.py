import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.database import get_db_connection
from sqlalchemy import text

db = get_db_connection()
if not db:
    print("No db")
    sys.exit(1)

with db.connect() as conn:
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Cyber_Evidence (
        EvidenceID INT AUTO_INCREMENT PRIMARY KEY,
        FIRNumber VARCHAR(50),
        IPAddress VARCHAR(50),
        CrimeType VARCHAR(100)
    );
    """))
    
    conn.execute(text("TRUNCATE TABLE Cyber_Evidence;"))
    
    conn.execute(text("""
    INSERT INTO Cyber_Evidence (FIRNumber, IPAddress, CrimeType) VALUES
    ('FIR-2026-001', '8.8.8.8', 'DDoS Attack'),
    ('FIR-2026-002', '1.1.1.1', 'Phishing Campaign'),
    ('FIR-2026-003', '93.184.216.34', 'Data Exfiltration');
    """))
    conn.commit()

print("Cyber evidence mock data injected")
