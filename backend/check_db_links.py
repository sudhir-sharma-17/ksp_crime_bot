import os
import mysql.connector
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_NAME = os.environ.get("DB_NAME", "KarnatakaPoliceFIRDB")
DB_PORT = int(os.environ.get("DB_PORT", "3306"))

print(f"Connecting to {DB_NAME}...")
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    port=DB_PORT
)
cursor = conn.cursor(dictionary=True)

queries = [
    ("1. Checking Unit Table (Are IDs strings or integers?):", "SELECT UnitID, UnitName FROM Unit LIMIT 10;"),
    ("2. Checking Employee Table (What units do they belong to?):", "SELECT DISTINCT UnitID FROM Employee;"),
    ("3. Checking CaseMaster Table (What stations have cases?):", "SELECT DISTINCT PoliceStationID FROM CaseMaster;"),
    ("4. Checking CaseCategory (Does 1 = Murder?):", "SELECT * FROM CaseCategory LIMIT 5;")
]

try:
    for title, query in queries:
        print(f"\n{'='*50}\n{title}\nQuery: {query}\n{'-'*50}")
        cursor.execute(query)
        results = cursor.fetchall()
        if not results:
            print("❌ No records found.")
        else:
            for row in results:
                print(row)
except mysql.connector.Error as err:
    print(f"❌ Database error: {err}")
finally:
    cursor.close()
    conn.close()
