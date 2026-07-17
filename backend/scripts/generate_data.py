import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker('en_IN') # Localized for India

# Setup
NUM_CASES = 1000
OUTPUT_FILE = 'insert_1000_records.sql'

def generate_sql():
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("USE KarnatakaPoliceFIRDB;\n")
        f.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")

        # ==========================================
        # 1. MASTER TABLES (Static Lookups)
        # ==========================================
        f.write("-- 1. Master Tables\n")
        f.write("INSERT IGNORE INTO State VALUES (29, 'Karnataka', 1, 1);\n")
        
        districts = [(443, 'Bengaluru City'), (444, 'Mysuru'), (445, 'Hubballi')]
        for d in districts:
            f.write(f"INSERT IGNORE INTO District VALUES ({d[0]}, '{d[1]}', 29, 1);\n")
            f.write(f"INSERT IGNORE INTO Court VALUES ({d[0]+10}, 'District Court {d[1]}', {d[0]}, 29, 1);\n")
            
        f.write("INSERT IGNORE INTO UnitType VALUES (1, 'Police Station', 'District', 5, 1);\n")
        
        # 10 Police Stations
        stations = []
        for i in range(1, 11):
            dist = random.choice(districts)[0]
            unit_id = 1000 + i
            stations.append((unit_id, dist))
            f.write(f"INSERT IGNORE INTO Unit VALUES ({unit_id}, '{fake.city()} PS', 1, NULL, 1, 29, {dist}, 1);\n")
            
        # Ranks & Designations
        f.write("INSERT IGNORE INTO `Rank` VALUES (3, 'Inspector', 10, 1), (4, 'Sub-Inspector', 12, 1);\n")
        f.write("INSERT IGNORE INTO Designation VALUES (1, 'SHO', 1, 1), (2, 'IO', 1, 2);\n")
        
        # Acts & Sections
        acts = [('IPC', 'Indian Penal Code', 'IPC'), ('IT_ACT', 'Information Technology Act', 'IT Act')]
        for a in acts:
            f.write(f"INSERT IGNORE INTO Act VALUES ('{a[0]}', '{a[1]}', '{a[2]}', 1);\n")
        f.write("INSERT IGNORE INTO Section VALUES ('302', 'IPC', 'Murder', 1), ('379', 'IPC', 'Theft', 1), ('66D', 'IT_ACT', 'Cheating', 1);\n")
        
        # Crime Heads
        f.write("INSERT IGNORE INTO CrimeHead VALUES (101, 'Crimes Against Body', 1), (102, 'Crimes Against Property', 1);\n")
        f.write("INSERT IGNORE INTO CrimeSubHead VALUES (201, 101, 'Murder', 1), (202, 102, 'Theft', 2);\n")
        
        # Categories & Statuses
        f.write("INSERT IGNORE INTO CaseCategory VALUES (1, 'FIR'), (3, 'UDR');\n")
        f.write("INSERT IGNORE INTO GravityOffence VALUES (1, 'Heinous'), (2, 'Non-Heinous');\n")
        f.write("INSERT IGNORE INTO CaseStatusMaster VALUES (1, 'Under Investigation'), (2, 'Charge Sheeted');\n")
        
        # Demographics
        f.write("INSERT IGNORE INTO CasteMaster VALUES (1, 'General'), (2, 'OBC'), (3, 'SC/ST');\n")
        f.write("INSERT IGNORE INTO ReligionMaster VALUES (1, 'Hindu'), (2, 'Muslim'), (3, 'Christian');\n")
        f.write("INSERT IGNORE INTO OccupationMaster VALUES (1, 'Private Employee'), (2, 'Business'), (3, 'Student');\n")

        # Generate 50 Employees
        f.write("\n-- 2. Employees\n")
        employees = []
        for i in range(1, 51):
            emp_id = 5000 + i
            employees.append(emp_id)
            station = random.choice(stations)
            f.write(f"INSERT IGNORE INTO Employee VALUES ({emp_id}, {station[1]}, {station[0]}, 4, 2, 'KGID{random.randint(1000,9999)}', '{fake.first_name()}', '1985-01-01', 1, 1, 0, '2010-01-01');\n")

        # ==========================================
        # 2. TRANSACTIONAL DATA (1000 Cases)
        # ==========================================
        f.write("\n-- 3. Case Master and Relational Data\n")
        
        for i in range(1, NUM_CASES + 1):
            # Case Master Variables
            case_id = 10000 + i
            station = random.choice(stations)
            emp = random.choice(employees)
            cat = random.choice([1, 3])
            year = random.randint(2023, 2026)
            
            # Format: 1 digit Category + 4 digit District + 4 digit Station + 4 digit Year + 5 digit Serial
            crime_no = f"{cat}{station[1]:04d}{station[0]:04d}{year}{i:05d}"
            case_no = f"{year}{i:05d}"
            
            reg_date = fake.date_between(start_date=f'-3y', end_date='today')
            inc_date = reg_date - timedelta(days=random.randint(0, 5))
            lat = round(random.uniform(12.0, 18.0), 6)
            lon = round(random.uniform(74.0, 78.0), 6)
            facts = fake.sentence(nb_words=15).replace("'", "''")
            
            # CaseMaster
            f.write(f"INSERT INTO CaseMaster VALUES ({case_id}, '{crime_no}', '{case_no}', '{reg_date}', {emp}, {station[0]}, {cat}, 1, 101, 201, 1, {station[1]+10}, '{inc_date} 10:00:00', '{inc_date} 11:00:00', '{reg_date} 09:00:00', {lat}, {lon}, '{facts}');\n")
            
            # Complainant
            f.write(f"INSERT INTO ComplainantDetails VALUES ({case_id+10000}, {case_id}, '{fake.name()}', {random.randint(20, 60)}, 1, 1, 1, 1);\n")
            
            # Victim
            f.write(f"INSERT INTO Victim VALUES ({case_id+20000}, {case_id}, '{fake.name()}', {random.randint(18, 70)}, 1, '0');\n")
            
            # Accused
            accused_id = case_id+30000
            f.write(f"INSERT INTO Accused VALUES ({accused_id}, {case_id}, '{fake.name()}', {random.randint(18, 55)}, 1, 'A1');\n")
            
            # Act/Section
            f.write(f"INSERT INTO ActSectionAssociation VALUES ({case_id}, 'IPC', '302', 1, 1);\n")
            
            # Arrest Surrender (50% chance of arrest)
            if random.choice([True, False]):
                f.write(f"INSERT INTO ArrestSurrender VALUES ({case_id+40000}, {case_id}, 1, '{reg_date}', 29, {station[1]}, {station[0]}, {emp}, {station[1]+10}, {accused_id}, 1, 0);\n")

        f.write("\nSET FOREIGN_KEY_CHECKS = 1;\n")

    print(f"Success! {OUTPUT_FILE} has been generated with {NUM_CASES} complete records.")

if __name__ == "__main__":
    generate_sql()
