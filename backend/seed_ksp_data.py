import os
import random
from datetime import datetime, timedelta
import mysql.connector
from faker import Faker
from dotenv import load_dotenv

# Initialize Faker with Indian locale for realistic names
fake = Faker('en_IN')

# Load environment variables
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_NAME = os.environ.get("DB_NAME", "KarnatakaPoliceFIRDB")
DB_PORT = int(os.environ.get("DB_PORT", "3306"))
print(f"Connecting to database: {DB_NAME} at {DB_HOST}...")

try:
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )
    cursor = conn.cursor()
    print("✅ Connected to MySQL successfully.")
except mysql.connector.Error as err:
    print(f"❌ Connection error: {err}")
    exit(1)

def get_valid_ids(table, id_column):
    cursor.execute(f"SELECT {id_column} FROM `{table}`")
    return [row[0] for row in cursor.fetchall()]

print("Fetching valid lookup IDs...")
valid_districts = get_valid_ids("District", "DistrictID")
valid_units = get_valid_ids("Unit", "UnitID")
valid_ranks = get_valid_ids("Rank", "RankID")
valid_designations = get_valid_ids("Designation", "DesignationID")
valid_case_categories = get_valid_ids("CaseCategory", "CaseCategoryID")
valid_gravity = get_valid_ids("GravityOffence", "GravityOffenceID")
valid_crime_heads = get_valid_ids("CrimeHead", "CrimeHeadID")
valid_crime_subheads = get_valid_ids("CrimeSubHead", "CrimeSubHeadID")
valid_case_status = get_valid_ids("CaseStatusMaster", "CaseStatusID")
valid_courts = get_valid_ids("Court", "CourtID")
valid_occupations = get_valid_ids("OccupationMaster", "OccupationID")
valid_religions = get_valid_ids("ReligionMaster", "ReligionID")
valid_castes = get_valid_ids("CasteMaster", "caste_master_id")

if not valid_units or not valid_districts:
    print("❌ Critical lookup tables (Unit, District) are empty! Cannot seed data.")
    exit(1)

print("Starting data seeding process...")

# ==========================================
# 1. SEED EMPLOYEES (50 Officers)
# ==========================================
print("Seeding 50 Employees...")
employees_data = []
for i in range(1, 51):
    employee_id = i
    district_id = random.choice(valid_districts)
    unit_id = random.choice(valid_units)
    rank_id = random.choice(valid_ranks) if valid_ranks else None
    designation_id = random.choice(valid_designations) if valid_designations else None
    kgid = f"KGID{random.randint(100000, 999999)}"
    first_name = fake.name()
    
    # Random DOB between 1970 and 1995
    start_dob = datetime.strptime("1970-01-01", "%Y-%m-%d")
    end_dob = datetime.strptime("1995-12-31", "%Y-%m-%d")
    employee_dob = start_dob + timedelta(days=random.randint(0, (end_dob - start_dob).days))
    
    gender_id = random.choice([1, 2]) # Assuming 1: Male, 2: Female
    blood_group_id = random.randint(1, 8)
    phys_chall = 0
    
    # Appointment date
    appointment_date = employee_dob + timedelta(days=random.randint(20*365, 30*365))
    
    employees_data.append((
        employee_id, district_id, unit_id, rank_id, designation_id,
        kgid, first_name, employee_dob, gender_id, blood_group_id,
        phys_chall, appointment_date
    ))

# Clear existing tables (in correct order due to foreign keys)
print("Clearing old data (transaction tables)...")
cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
cursor.execute("TRUNCATE TABLE ChargesheetDetails;")
cursor.execute("TRUNCATE TABLE ComplainantDetails;")
cursor.execute("TRUNCATE TABLE Victim;")
cursor.execute("TRUNCATE TABLE Accused;")
cursor.execute("TRUNCATE TABLE CaseMaster;")
cursor.execute("TRUNCATE TABLE Employee;")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
conn.commit()

emp_query = """
INSERT INTO Employee 
(EmployeeID, DistrictID, UnitID, RankID, DesignationID, KGID, FirstName, EmployeeDOB, GenderID, BloodGroupID, PhysicallyChallenged, AppointmentDate) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
cursor.executemany(emp_query, employees_data)
conn.commit()
print("✅ Inserted 50 Employees.")

# ==========================================
# 2. SEED CASES (500 Cases)
# ==========================================
print("Seeding 500 CaseMasters...")
cases_data = []
accused_data = []
victim_data = []
complainant_data = []
chargesheet_data = []

accused_id_counter = 1
victim_id_counter = 1
complainant_id_counter = 1
chargesheet_id_counter = 1

for case_id in range(1, 501):
    crime_no = f"{random.randint(1, 200)}/202{random.randint(4, 6)}"
    case_no = f"KSP-CASE-{case_id}-{random.randint(1000,9999)}"
    
    # Register date in 2024, 2025, or 2026
    reg_start = datetime.strptime("2024-01-01", "%Y-%m-%d")
    reg_end = datetime.strptime("2026-06-01", "%Y-%m-%d")
    reg_date = reg_start + timedelta(days=random.randint(0, (reg_end - reg_start).days))
    
    police_person_id = random.randint(1, 50)
    police_station_id = random.choice(valid_units)
    case_category_id = random.choice(valid_case_categories) if valid_case_categories else None
    gravity_offence_id = random.choice(valid_gravity) if valid_gravity else None
    crime_major_id = random.choice(valid_crime_heads) if valid_crime_heads else None
    crime_minor_id = random.choice(valid_crime_subheads) if valid_crime_subheads else None
    case_status_id = random.choice(valid_case_status) if valid_case_status else None
    court_id = random.choice(valid_courts) if valid_courts else None
    
    # Incident dates
    incident_from = reg_date - timedelta(days=random.randint(1, 30))
    incident_to = incident_from + timedelta(hours=random.randint(1, 48))
    
    # Random locations around Karnataka
    lat = round(random.uniform(11.5, 18.5), 6)
    lon = round(random.uniform(74.0, 78.5), 6)
    
    brief_facts = fake.paragraph(nb_sentences=3)
    
    cases_data.append((
        case_id, crime_no, case_no, reg_date.date(), police_person_id, police_station_id,
        case_category_id, gravity_offence_id, crime_major_id, crime_minor_id,
        case_status_id, court_id, incident_from, incident_to, reg_date, lat, lon, brief_facts
    ))
    
    # Generate 1 to 3 Accused per case
    for _ in range(random.randint(1, 3)):
        accused_data.append((
            accused_id_counter, case_id, fake.name(), random.randint(18, 65),
            random.choice([1, 2]), f"PID-{random.randint(1000,9999)}"
        ))
        accused_id_counter += 1
        
    # Generate 1 to 2 Victims per case
    for _ in range(random.randint(1, 2)):
        victim_data.append((
            victim_id_counter, case_id, fake.name(), random.randint(5, 80),
            random.choice([1, 2]), "No"
        ))
        victim_id_counter += 1
        
    # Generate 1 Complainant per case
    complainant_data.append((
        complainant_id_counter, case_id, fake.name(), random.randint(18, 70),
        random.choice(valid_occupations) if valid_occupations else None,
        random.choice(valid_religions) if valid_religions else None,
        random.choice(valid_castes) if valid_castes else None,
        random.choice([1, 2])
    ))
    complainant_id_counter += 1
    
    # Generate Chargesheet for half the cases
    if random.choice([True, False]):
        chargesheet_data.append((
            chargesheet_id_counter, case_id,
            reg_date + timedelta(days=random.randint(10, 90)),
            random.choice(['A', 'B', 'C']), police_person_id
        ))
        chargesheet_id_counter += 1

case_query = """
INSERT INTO CaseMaster 
(CaseMasterID, CrimeNo, CaseNo, CrimeRegisteredDate, PolicePersonID, PoliceStationID, 
CaseCategoryID, GravityOffenceID, CrimeMajorHeadID, CrimeMinorHeadID, CaseStatusID, CourtID, 
IncidentFromDate, IncidentToDate, InfoReceivedPSDate, latitude, longitude, BriefFacts) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
cursor.executemany(case_query, cases_data)
conn.commit()
print("✅ Inserted 500 CaseMasters.")

# ==========================================
# 3. SEED RELATED ENTITIES
# ==========================================
print("Seeding Accused, Victims, ComplainantDetails, and Chargesheets...")

accused_query = "INSERT INTO Accused (AccusedMasterID, CaseMasterID, AccusedName, AgeYear, GenderID, PersonID) VALUES (%s, %s, %s, %s, %s, %s)"
cursor.executemany(accused_query, accused_data)

victim_query = "INSERT INTO Victim (VictimMasterID, CaseMasterID, VictimName, AgeYear, GenderID, VictimPolice) VALUES (%s, %s, %s, %s, %s, %s)"
cursor.executemany(victim_query, victim_data)

comp_query = "INSERT INTO ComplainantDetails (ComplainantID, CaseMasterID, ComplainantName, AgeYear, OccupationID, ReligionID, CasteID, GenderID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
cursor.executemany(comp_query, complainant_data)

cs_query = "INSERT INTO ChargesheetDetails (CSID, CaseMasterID, csdate, cstype, PolicePersonID) VALUES (%s, %s, %s, %s, %s)"
cursor.executemany(cs_query, chargesheet_data)

conn.commit()
print(f"✅ Inserted {len(accused_data)} Accused.")
print(f"✅ Inserted {len(victim_data)} Victims.")
print(f"✅ Inserted {len(complainant_data)} Complainants.")
print(f"✅ Inserted {len(chargesheet_data)} Chargesheets.")

print("🎉 All mock data seeded successfully!")
cursor.close()
conn.close()
