import os
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_NAME = os.environ.get("DB_NAME", "KarnatakaPoliceFIRDB")
DB_PORT = int(os.environ.get("DB_PORT", "3306"))

print("Connecting to database for Golden Records Injection...")
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    port=DB_PORT
)
cursor = conn.cursor()

# Get the next available IDs to avoid PK clashes
cursor.execute("SELECT MAX(EmployeeID) FROM Employee")
next_emp_id = (cursor.fetchone()[0] or 0) + 1

cursor.execute("SELECT MAX(CaseMasterID) FROM CaseMaster")
next_case_id = (cursor.fetchone()[0] or 0) + 1

cursor.execute("SELECT MAX(VictimMasterID) FROM Victim")
next_victim_id = (cursor.fetchone()[0] or 0) + 1

# ==========================================
# Scenario 1: Specific Lookup for Hubballi (445)
# ==========================================
print("Injecting Scenario 1 (Hubballi / Inspector Ravi Kumar)...")

# Unit 1001 is mapped to Hubballi (445) in our lookup check
emp_query = """
INSERT INTO Employee (EmployeeID, DistrictID, UnitID, FirstName) 
VALUES (%s, %s, %s, %s)
"""
cursor.execute(emp_query, (next_emp_id, 445, 1001, "Inspector Ravi Kumar"))
ravi_kumar_id = next_emp_id
next_emp_id += 1

case_query = """
INSERT INTO CaseMaster 
(CaseMasterID, CrimeNo, CaseNo, PolicePersonID, PoliceStationID, CrimeRegisteredDate, BriefFacts) 
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""
cursor.execute(case_query, (
    next_case_id, 
    "104431001202400001", 
    f"KSP-CASE-{next_case_id}",
    ravi_kumar_id, 
    1001, 
    datetime.now().date(), 
    "Theft of gold chain at Majestic bus stand."
))
next_case_id += 1

# ==========================================
# Scenario 2: Analytical Grouping for Bengaluru (443)
# ==========================================
print("Injecting Scenario 2 (Bengaluru Heinous Crimes)...")

# Unit 1004 is mapped to Bengaluru City (443)
# GravityOffenceID 1 is Heinous Crimes
for i in range(3):
    cursor.execute(case_query, (
        next_case_id,
        f"BLR-2026-HEINOUS-{i}",
        f"KSP-CASE-{next_case_id}",
        ravi_kumar_id, # Reuse inspector for simplicity
        1004,
        datetime(2026, random_month:=5, 10).date(),
        "Heinous crime scenario in Bengaluru City."
    ))
    
    # Update GravityOffenceID to 1 explicitly for this case
    cursor.execute("UPDATE CaseMaster SET GravityOffenceID = 1 WHERE CaseMasterID = %s", (next_case_id,))
    next_case_id += 1

# ==========================================
# Scenario 3: Complex Join - Murder in Mysuru (444)
# ==========================================
print("Injecting Scenario 3 (Mysuru Murder - IPC 302)...")

# Check if Act 'IPC' exists, if not create
cursor.execute("SELECT ActCode FROM Act WHERE ActCode = 'IPC'")
if not cursor.fetchone():
    cursor.execute("INSERT INTO Act (ActCode, ActDescription, ShortName) VALUES ('IPC', 'Indian Penal Code', 'IPC')")

# Check if Section '302' exists, if not create
cursor.execute("SELECT SectionCode FROM Section WHERE SectionCode = '302' AND ActCode = 'IPC'")
if not cursor.fetchone():
    cursor.execute("INSERT INTO Section (SectionCode, ActCode, SectionDescription) VALUES ('302', 'IPC', 'Punishment for murder')")

# Unit 1006 is mapped to Mysuru (444)
cursor.execute(case_query, (
    next_case_id,
    "MYS-2026-MURDER-1",
    f"KSP-CASE-{next_case_id}",
    ravi_kumar_id,
    1006,
    datetime.now().date(),
    "Murder case in Mysuru."
))
mysuru_case_id = next_case_id
next_case_id += 1

# Link Act and Section to Case
act_sec_query = """
INSERT INTO ActSectionAssociation (CaseMasterID, ActID, SectionID, ActOrderID, SectionOrderID) 
VALUES (%s, %s, %s, %s, %s)
"""
cursor.execute(act_sec_query, (mysuru_case_id, 'IPC', '302', 1, 1))

# ==========================================
# Scenario 4: Investigative - Minor Victim
# ==========================================
print("Injecting Scenario 4 (Minor Victim)...")

cursor.execute(case_query, (
    next_case_id,
    "MINOR-VICTIM-2026-1",
    f"KSP-CASE-{next_case_id}",
    ravi_kumar_id,
    1004, # Bengaluru
    datetime.now().date(),
    "Case involving a minor victim."
))
minor_case_id = next_case_id
next_case_id += 1

victim_query = """
INSERT INTO Victim (VictimMasterID, CaseMasterID, VictimName, AgeYear, GenderID) 
VALUES (%s, %s, %s, %s, %s)
"""
cursor.execute(victim_query, (next_victim_id, minor_case_id, "Jane Doe (Minor)", 14, 2))
next_victim_id += 1

# Commit all changes
conn.commit()
print("🎉 Golden Records successfully injected into the database!")

cursor.close()
conn.close()
