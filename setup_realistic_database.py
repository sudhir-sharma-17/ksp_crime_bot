import os
import sys
import gc
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path
import mysql.connector
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# Ensure required libraries are installed
try:
    from faker import Faker
    from dotenv import load_dotenv
except ImportError:
    print("[ERROR] Critical dependencies missing. Please install them first:")
    print("   pip install faker python-dotenv mysql-connector-python sqlalchemy pymysql")
    sys.exit(1)

# Locate directories relative to this setup script
BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR / "backend"
ENV_PATH = BACKEND_DIR / ".env"

if not ENV_PATH.exists():
    print("[ERROR] backend/.env was not found. Please create it with DB credentials first.")
    sys.exit(1)

# Load environment variables
load_dotenv(dotenv_path=ENV_PATH)

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_NAME = os.environ.get("DB_NAME", "KarnatakaPoliceFIRDB")
DB_PORT = int(os.environ.get("DB_PORT", "3306"))

print("=" * 70)
print("STARTING REALISTIC DATABASE SEEDING (LOGICALLY LINKED DATA & REAL GENDERS)")
print(f"   Database: {DB_NAME}")
print(f"   Host:     {DB_HOST}:{DB_PORT}")
print("=" * 70)

# Connect to database
try:
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )
    cursor = conn.cursor()
    print("[INFO] Connected to MySQL successfully.")
except Exception as e:
    print(f"[ERROR] Connection error: {e}")
    sys.exit(1)

# Realistic Names for Gender Consistency
MALE_NAMES = [
    "Rajesh Kumar", "Amit Sharma", "Suresh Patil", "Karan Singh", "Vijay Mishra",
    "Arjun Nair", "Rahul Reddy", "Sunil Gowda", "Vikram Joshi", "Sanjay Dutt",
    "Ramesh Hegde", "Anand Prasad", "Manjunath Prasad", "Ganesh Naik", "Santhosh Kumar",
    "Prakash Rao", "Mohan Lal", "Harish Gowda", "Pradeep Kumar", "Kiran Murthy",
    "Abhishek Hegde", "Sandeep Patil", "Raghavendra Rao", "Chethan Kumar", "Naveen Raj"
]

FEMALE_NAMES = [
    "Sunita Sharma", "Anjali Rao", "Priya Rao", "Sneha Rao", "Deepa Gowda",
    "Kavita Nair", "Pooja Patil", "Divya Joshi", "Meera Reddy", "Shruthi Naik",
    "Saritha Hegde", "Lakshmi Prasanna", "Asha Devi", "Geetha Murthy", "Sujatha Rao",
    "Preethi Hegde", "Radha Krishna", "Swathi Kumar", "Rekha Naik", "Roopa Gowda",
    "Uma Maheshwari", "Nandini Raj", "Vidya Sagar", "Bhagya Lakshmi", "Savitha Murthy"
]

POLICE_STATIONS = [
    # Bengaluru City (443)
    {"id": 1001, "name": "Koramangala Police Station", "district": 443},
    {"id": 1002, "name": "Indiranagar Police Station", "district": 443},
    {"id": 1003, "name": "Whitefield Police Station", "district": 443},
    {"id": 1004, "name": "HSR Layout Police Station", "district": 443},
    # Mysuru (444)
    {"id": 1005, "name": "Devaraja Police Station", "district": 444},
    {"id": 1006, "name": "Lashkar Police Station", "district": 444},
    {"id": 1007, "name": "Vidyaranyapuram Police Station", "district": 444},
    # Hubballi (445)
    {"id": 1008, "name": "Hubballi Suburban Police Station", "district": 445},
    {"id": 1009, "name": "Gokul Road Police Station", "district": 445},
    {"id": 1010, "name": "Hubballi Town Police Station", "district": 445}
]

# Crime Types mapped to Acts & Sections and realistic descriptions
CRIME_PROFILES = [
    {
        "type": "Theft",
        "act": "IPC",
        "section": "379",
        "crime_head": 102, # Crimes Against Property
        "crime_subhead": 202,
        "facts_templates": [
            "Complainant reported that some unknown persons entered their house at night and stole gold ornaments weighing {param} grams and cash.",
            "Complainant parked their two-wheeler bearing registration number KA-03-EX-{param} near the market, and found it missing when they returned.",
            "Unidentified thieves broke the lock of a shop and stole electronic items and laptop computers valued at {param} rupees."
        ]
    },
    {
        "type": "Murder",
        "act": "IPC",
        "section": "302",
        "crime_head": 101, # Crimes Against Body
        "crime_subhead": 201,
        "facts_templates": [
            "Information was received that a male dead body aged around {param} was found near the highway with severe stab wounds on the chest.",
            "A physical dispute arose between two groups over a property land line, during which the accused assaulted the victim with a sharp weapon, causing instantaneous death.",
            "The victim was found murdered inside their residence. The body had severe neck injuries inflicted with a sharp knife."
        ]
    },
    {
        "type": "Cyber Fraud",
        "act": "IT_ACT",
        "section": "66D",
        "crime_head": 102, # Crimes Against Property
        "crime_subhead": 202,
        "facts_templates": [
            "The complainant received a phishing link via SMS offering rewards, and after clicking it, {param} rupees were fraudulently debited from their bank account.",
            "Accused called the complainant posing as a bank customer service representative, obtained the OTP, and transferred {param} rupees from their wallet.",
            "Complainant was cheated online by a fraudulent investment scheme through a social media advertisement, losing {param} rupees."
        ]
    },
    {
        "type": "Assault / Physical Altercation",
        "act": "IPC",
        "section": "324",
        "crime_head": 101, # Crimes Against Body
        "crime_subhead": 201,
        "facts_templates": [
            "Accused pick up a sudden argument with the victim regarding a parking issue and assaulted them with a wooden stick, causing {param} injuries.",
            "A verbal dispute escalated in public, during which the accused physically assaulted the victim and threatened them with dire consequences.",
            "Accused intentionally intercepted the victim's way and beat them up with iron rods, causing severe contusions and hospitalization."
        ]
    }
]

# Set foreign keys check to 0 to safely re-create/clean tables
cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

# Create tables if they do not exist (critical for new/empty DB instances like Railway)
cursor.execute("DROP TABLE IF EXISTS State;")
cursor.execute("CREATE TABLE IF NOT EXISTS State (StateID INT PRIMARY KEY, StateName VARCHAR(255), NationalityID INT, Active BIT);")
cursor.execute("CREATE TABLE IF NOT EXISTS District (DistrictID INT PRIMARY KEY, DistrictName VARCHAR(255), StateID INT, Active BIT);")
cursor.execute("CREATE TABLE IF NOT EXISTS Court (CourtID INT PRIMARY KEY, CourtName VARCHAR(255), DistrictID INT, StateID INT, Active BIT);")
cursor.execute("CREATE TABLE IF NOT EXISTS Unit (UnitID INT PRIMARY KEY, UnitName VARCHAR(255), TypeID INT, ParentUnit INT, NationalityID INT, StateID INT, DistrictID INT, Active BIT);")
cursor.execute("DROP TABLE IF EXISTS `Rank`;")
cursor.execute("CREATE TABLE IF NOT EXISTS `Rank` (RankID INT PRIMARY KEY, RankDescription VARCHAR(255), RankOrder INT, Active BIT);")
cursor.execute("DROP TABLE IF EXISTS Designation;")
cursor.execute("CREATE TABLE IF NOT EXISTS Designation (DesignationID INT PRIMARY KEY, DesignationDescription VARCHAR(255), DesignationOrder INT, Active BIT);")
cursor.execute("CREATE TABLE IF NOT EXISTS Act (ActCode VARCHAR(50) PRIMARY KEY, ActDescription VARCHAR(255), ShortName VARCHAR(100), Active BIT);")
cursor.execute("CREATE TABLE IF NOT EXISTS Section (ActCode VARCHAR(50), SectionCode VARCHAR(50), SectionDescription VARCHAR(255), Active BIT, PRIMARY KEY (ActCode, SectionCode));")
cursor.execute("CREATE TABLE IF NOT EXISTS CrimeHead (CrimeHeadID INT PRIMARY KEY, CrimeGroupName VARCHAR(255), Active BIT);")
cursor.execute("CREATE TABLE IF NOT EXISTS CrimeSubHead (CrimeSubHeadID INT PRIMARY KEY, CrimeHeadID INT, CrimeSubHeadName VARCHAR(255), Active BIT);")
cursor.execute("CREATE TABLE IF NOT EXISTS CaseCategory (CaseCategoryID INT PRIMARY KEY, CaseCategoryName VARCHAR(255));")
cursor.execute("CREATE TABLE IF NOT EXISTS GravityOffence (GravityOffenceID INT PRIMARY KEY, GravityOffenceName VARCHAR(255));")
cursor.execute("CREATE TABLE IF NOT EXISTS CaseStatusMaster (CaseStatusID INT PRIMARY KEY, CaseStatusName VARCHAR(255));")
cursor.execute("CREATE TABLE IF NOT EXISTS CasteMaster (caste_master_id INT PRIMARY KEY, caste_master_name VARCHAR(100));")
cursor.execute("CREATE TABLE IF NOT EXISTS ReligionMaster (ReligionID INT PRIMARY KEY, ReligionName VARCHAR(100));")
cursor.execute("CREATE TABLE IF NOT EXISTS OccupationMaster (OccupationID INT PRIMARY KEY, OccupationName VARCHAR(100));")
cursor.execute("CREATE TABLE IF NOT EXISTS Employee (EmployeeID INT PRIMARY KEY, DistrictID INT, UnitID INT, RankID INT, DesignationID INT, KGID VARCHAR(50), FirstName VARCHAR(255), EmployeeDOB DATE, GenderID VARCHAR(10), BloodGroupID INT, PhysicallyChallenged INT, AppointmentDate DATE);")
cursor.execute("CREATE TABLE IF NOT EXISTS CaseMaster (CaseMasterID INT PRIMARY KEY, CrimeNo VARCHAR(50), CaseNo VARCHAR(50), CrimeRegisteredDate DATE, PolicePersonID INT, PoliceStationID INT, CaseCategoryID INT, GravityOffenceID INT, CrimeMajorHeadID INT, CrimeMinorHeadID INT, CaseStatusID INT, CourtID INT, IncidentFromDate DATETIME, IncidentToDate DATETIME, InfoReceivedPSDate DATETIME, latitude DOUBLE, longitude DOUBLE, BriefFacts TEXT);")
cursor.execute("CREATE TABLE IF NOT EXISTS Accused (AccusedMasterID INT PRIMARY KEY, CaseMasterID INT, AccusedName VARCHAR(255), AgeYear INT, GenderID VARCHAR(10), PersonID VARCHAR(50));")
cursor.execute("CREATE TABLE IF NOT EXISTS Victim (VictimMasterID INT PRIMARY KEY, CaseMasterID INT, VictimName VARCHAR(255), AgeYear INT, GenderID VARCHAR(10), VictimPolice VARCHAR(10));")
cursor.execute("CREATE TABLE IF NOT EXISTS ComplainantDetails (ComplainantID INT PRIMARY KEY, CaseMasterID INT, ComplainantName VARCHAR(255), AgeYear INT, OccupationID INT, ReligionID INT, CasteID INT, GenderID VARCHAR(10));")
cursor.execute("CREATE TABLE IF NOT EXISTS ChargesheetDetails (CSID INT PRIMARY KEY, CaseMasterID INT, csdate DATE, cstype VARCHAR(50), PolicePersonID INT);")
cursor.execute("CREATE TABLE IF NOT EXISTS ActSectionAssociation (CaseMasterID INT, ActID VARCHAR(50), SectionID VARCHAR(50), ActOrderID INT, SectionOrderID INT, PRIMARY KEY (CaseMasterID, ActID, SectionID));")
cursor.execute("CREATE TABLE IF NOT EXISTS Cyber_Evidence (EvidenceID INT AUTO_INCREMENT PRIMARY KEY, FIRNumber VARCHAR(50), IPAddress VARCHAR(50), CrimeType VARCHAR(100));")

# Safely truncate all tables
cursor.execute("TRUNCATE TABLE Accused;")
cursor.execute("TRUNCATE TABLE Victim;")
cursor.execute("TRUNCATE TABLE ComplainantDetails;")
cursor.execute("TRUNCATE TABLE ChargesheetDetails;")
cursor.execute("TRUNCATE TABLE ActSectionAssociation;")
cursor.execute("TRUNCATE TABLE CaseMaster;")
cursor.execute("TRUNCATE TABLE Employee;")
cursor.execute("TRUNCATE TABLE Unit;")
cursor.execute("TRUNCATE TABLE Court;")
cursor.execute("TRUNCATE TABLE District;")
cursor.execute("TRUNCATE TABLE State;")
cursor.execute("TRUNCATE TABLE Act;")
cursor.execute("TRUNCATE TABLE Section;")
cursor.execute("TRUNCATE TABLE CrimeHead;")
cursor.execute("TRUNCATE TABLE CrimeSubHead;")

cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
cursor.execute("ALTER TABLE Accused MODIFY COLUMN GenderID VARCHAR(10);")
cursor.execute("ALTER TABLE Victim MODIFY COLUMN GenderID VARCHAR(10);")
cursor.execute("ALTER TABLE ComplainantDetails MODIFY COLUMN GenderID VARCHAR(10);")
cursor.execute("ALTER TABLE Employee MODIFY COLUMN GenderID VARCHAR(10);")
conn.commit()

print("[INFO] Database transaction & master tables cleared, and GenderID columns altered to VARCHAR.")

# 1. Seed Master Tables
cursor.execute("INSERT IGNORE INTO State VALUES (29, 'Karnataka', 1, 1);")
districts = [(443, 'Bengaluru City'), (444, 'Mysuru'), (445, 'Hubballi')]
for dist_id, dist_name in districts:
    cursor.execute("INSERT IGNORE INTO District VALUES (%s, %s, 29, 1);", (dist_id, dist_name))
    cursor.execute("INSERT IGNORE INTO Court VALUES (%s, %s, %s, 29, 1);", (dist_id + 10, f"District Court {dist_name}", dist_id))

# Seed Stations
for ps in POLICE_STATIONS:
    cursor.execute("INSERT INTO Unit VALUES (%s, %s, 1, NULL, 1, 29, %s, 1);", (ps["id"], ps["name"], ps["district"]))

# Seed Ranks & Designations
cursor.execute("INSERT IGNORE INTO `Rank` VALUES (3, 'Inspector', 10, 1), (4, 'Sub-Inspector', 12, 1);")
cursor.execute("INSERT IGNORE INTO Designation VALUES (1, 'SHO', 1, 1), (2, 'IO', 1, 2);")

# Seed Acts & Sections
cursor.execute("INSERT IGNORE INTO Act VALUES ('IPC', 'Indian Penal Code', 'IPC', 1), ('IT_ACT', 'Information Technology Act', 'IT Act', 1);")
cursor.execute("INSERT IGNORE INTO Section (ActCode, SectionCode, SectionDescription, Active) VALUES ('IPC', '302', 'Murder', 1), ('IPC', '379', 'Theft', 1), ('IT_ACT', '66D', 'Cheating by Personation using Computer Resource', 1), ('IPC', '324', 'Voluntarily causing hurt by dangerous weapons', 1);")

# Crime Heads & Sub-Heads
cursor.execute("INSERT IGNORE INTO CrimeHead VALUES (101, 'Crimes Against Body', 1), (102, 'Crimes Against Property', 1);")
cursor.execute("INSERT IGNORE INTO CrimeSubHead VALUES (201, 101, 'Violent Crimes', 1), (202, 102, 'Thefts and Financial Crimes', 2);")

# Basic Lookups
cursor.execute("INSERT IGNORE INTO CaseCategory VALUES (1, 'FIR'), (3, 'UDR');")
cursor.execute("INSERT IGNORE INTO GravityOffence VALUES (1, 'Heinous'), (2, 'Non-Heinous');")
cursor.execute("INSERT IGNORE INTO CaseStatusMaster VALUES (1, 'Under Investigation'), (2, 'Charge Sheeted');")
cursor.execute("INSERT IGNORE INTO CasteMaster VALUES (1, 'General'), (2, 'OBC'), (3, 'SC/ST');")
cursor.execute("INSERT IGNORE INTO ReligionMaster VALUES (1, 'Hindu'), (2, 'Muslim'), (3, 'Christian');")
cursor.execute("INSERT IGNORE INTO OccupationMaster VALUES (1, 'Private Employee'), (2, 'Business'), (3, 'Student'), (4, 'Unemployed');")

conn.commit()
print("[INFO] Seeding standard Lookups and Police Stations finished.")

# 2. Seed 50 Employees / Officers with full realistic names
employees = []
for i in range(1, 51):
    emp_id = i
    ps = random.choice(POLICE_STATIONS)
    rank = random.choice([3, 4])
    desg = 1 if rank == 3 else 2
    
    # Generate realistic full names for officers
    is_male_emp = random.choice([True, False])
    name = random.choice(MALE_NAMES) if is_male_emp else random.choice(FEMALE_NAMES)
    emp_gender = 'Male' if is_male_emp else 'Female'
    kgid = f"KGID{random.randint(100000, 999999)}"
    
    cursor.execute("""
    INSERT INTO Employee 
    (EmployeeID, DistrictID, UnitID, RankID, DesignationID, KGID, FirstName, EmployeeDOB, GenderID, BloodGroupID, PhysicallyChallenged, AppointmentDate) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, (emp_id, ps["district"], ps["id"], rank, desg, kgid, name, "1985-06-15", emp_gender, 1, 0, "2010-01-10"))
    employees.append((emp_id, ps["id"], ps["district"]))

conn.commit()
print("[INFO] Seeded 50 Officers with realistic full names and string genders.")

# 3. Seed 500 Cases with logical relationships (Batched for instant remote database import)
accused_id = 1
victim_id = 1
comp_id = 1
cs_id = 1

case_master_rows = []
act_section_rows = []
accused_rows = []
victim_rows = []
complainant_rows = []
chargesheet_rows = []

for case_id in range(1, 501):
    profile = random.choice(CRIME_PROFILES)
    officer = random.choice(employees)
    
    reg_start = datetime.strptime("2024-01-01", "%Y-%m-%d")
    reg_end = datetime.strptime("2026-06-01", "%Y-%m-%d")
    reg_date = reg_start + timedelta(days=random.randint(0, (reg_end - reg_start).days))
    incident_date = reg_date - timedelta(days=random.randint(1, 5))
    
    crime_no = f"{case_id:04d}/202{random.randint(4, 6)}"
    case_no = f"KSP-CASE-{case_id:04d}"
    
    # Custom facts parameters to make descriptions realistic
    if profile["type"] == "Theft":
        param = str(random.choice([10, 20, 50, 100]))
    elif profile["type"] == "Murder":
        param = f"{random.randint(25, 60)}"
    elif profile["type"] == "Cyber Fraud":
        param = f"{random.randint(10000, 500000):,}"
    else:
        param = f"{random.randint(1, 3)}"
        
    brief_facts = random.choice(profile["facts_templates"]).format(param=param)
    
    lat = round(random.uniform(12.5, 18.0), 6)
    lon = round(random.uniform(74.0, 78.0), 6)
    
    # Collect CaseMaster Row
    case_master_rows.append((
        case_id, crime_no, case_no, reg_date.date(), officer[0], officer[1], 
        1, 1 if profile["type"] == "Murder" else 2, profile["crime_head"], profile["crime_subhead"], 
        1, officer[2] + 10, incident_date, incident_date + timedelta(hours=2), reg_date, lat, lon, brief_facts
    ))
          
    # Collect primary Act & Section Association
    act_section_rows.append((case_id, profile["act"], profile["section"], 1, 1))
    
    # 30% chance of adding a second, logical act/section association to vary ActOrderID and SectionOrderID
    if random.random() < 0.3:
        if profile["type"] == "Murder":
            # Add assault under same Act (IPC), so ActOrderID=1, SectionOrderID=2
            act_section_rows.append((case_id, 'IPC', '324', 1, 2))
        elif profile["type"] == "Cyber Fraud":
            # Add theft under different Act (IPC), so ActOrderID=2, SectionOrderID=1
            act_section_rows.append((case_id, 'IPC', '379', 2, 1))
        elif profile["type"] == "Theft":
            # Add assault under same Act (IPC), so ActOrderID=1, SectionOrderID=2
            act_section_rows.append((case_id, 'IPC', '324', 1, 2))
        elif profile["type"] == "Assault / Physical Altercation":
            # Add theft under same Act (IPC), so ActOrderID=1, SectionOrderID=2
            act_section_rows.append((case_id, 'IPC', '379', 1, 2))
    
    # Collect Accused Row
    is_male = random.choice([True, False])
    acc_name = random.choice(MALE_NAMES) if is_male else random.choice(FEMALE_NAMES)
    acc_gender = 'Male' if is_male else 'Female'
    accused_rows.append((accused_id, case_id, acc_name, random.randint(18, 60), acc_gender, f"ACC-{accused_id:04d}"))
    accused_id += 1
    
    # Collect Victim Row
    is_male_v = random.choice([True, False])
    vic_name = random.choice(MALE_NAMES) if is_male_v else random.choice(FEMALE_NAMES)
    vic_gender = 'Male' if is_male_v else 'Female'
    victim_rows.append((victim_id, case_id, vic_name, random.randint(10, 80), vic_gender, "No"))
    victim_id += 1
    
    # Collect Complainant Row
    is_male_c = random.choice([True, False])
    comp_name = random.choice(MALE_NAMES) if is_male_c else random.choice(FEMALE_NAMES)
    comp_gender = 'Male' if is_male_c else 'Female'
    complainant_rows.append((
        comp_id, case_id, comp_name, random.randint(18, 70), 
        random.choice([1, 2, 3]), random.choice([1, 2]), random.choice([1, 2]), comp_gender
    ))
    comp_id += 1
    
    # Collect Chargesheet Row
    if random.choice([True, False]):
        chargesheet_rows.append((cs_id, case_id, reg_date + timedelta(days=30), 'A', officer[0]))
        cs_id += 1

print("[INFO] Performing bulk database insertions...")
# Bulk insert CaseMaster
cursor.executemany("""
INSERT INTO CaseMaster 
(CaseMasterID, CrimeNo, CaseNo, CrimeRegisteredDate, PolicePersonID, PoliceStationID, 
CaseCategoryID, GravityOffenceID, CrimeMajorHeadID, CrimeMinorHeadID, CaseStatusID, CourtID, 
IncidentFromDate, IncidentToDate, InfoReceivedPSDate, latitude, longitude, BriefFacts) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
""", case_master_rows)

# Bulk insert ActSectionAssociation
cursor.executemany("""
INSERT INTO ActSectionAssociation (CaseMasterID, ActID, SectionID, ActOrderID, SectionOrderID)
VALUES (%s, %s, %s, %s, %s);
""", act_section_rows)

# Bulk insert Accused
cursor.executemany("""
INSERT INTO Accused (AccusedMasterID, CaseMasterID, AccusedName, AgeYear, GenderID, PersonID) 
VALUES (%s, %s, %s, %s, %s, %s);
""", accused_rows)

# Bulk insert Victim
cursor.executemany("""
INSERT INTO Victim (VictimMasterID, CaseMasterID, VictimName, AgeYear, GenderID, VictimPolice) 
VALUES (%s, %s, %s, %s, %s, %s);
""", victim_rows)

# Bulk insert ComplainantDetails
cursor.executemany("""
INSERT INTO ComplainantDetails (ComplainantID, CaseMasterID, ComplainantName, AgeYear, OccupationID, ReligionID, CasteID, GenderID) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
""", complainant_rows)

# Bulk insert ChargesheetDetails
cursor.executemany("""
INSERT INTO ChargesheetDetails (CSID, CaseMasterID, csdate, cstype, PolicePersonID) 
VALUES (%s, %s, %s, %s, %s);
""", chargesheet_rows)

conn.commit()
print(f"[INFO] Seeding finished. Generated {accused_id - 1} accused, {victim_id - 1} victims, and {case_id} realistic cases in bulk.")
cursor.close()
conn.close()

print("=" * 70)
print("REALISTIC SEED DATA COMPLETED SUCCESSFULLY!")
print("=" * 70)
