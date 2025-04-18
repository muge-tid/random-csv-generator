import csv
import random
import os
import re
from datetime import datetime, timedelta
from faker import Faker
import unicodedata

# Country and locale settings
faker_locales = {
    "DE": "de_DE", "IN": "en_IN", "TR": "tr_TR", "UK": "en_GB",
    "US": "en_US", "FR": "fr_FR"
}
country_codes = {
    "DE": "+49", "IN": "+91", "TR": "+90", "UK": "+44",
    "US": "+1", "FR": "+33"
}

# Departments and job titles
departments_jobs = {
    "Engineering": ["Software Engineer", "QA Engineer", "DevOps Engineer", "Engineering Lead"],
    "Marketing": ["Content Specialist", "SEO Specialist", "Marketing Lead"],
    "Sales": ["Sales Executive", "Account Manager", "Sales Lead"],
    "HR": ["Recruiter", "HR Coordinator", "HR Manager"],
    "Finance": ["Accountant", "Financial Analyst", "Finance Manager"],
    "Executive": ["CEO"]
}

# Helper functions
def random_date(start, end, date_format="%d/%m/%Y"):
    delta = end - start
    return (start + timedelta(days=random.randint(0, delta.days))).strftime(date_format)

def generate_phone_number(country_code):
    number = ''.join(random.choices("0123456789", k=10))
    return f"{country_code}{number}"

def sanitize_name(name):
    nfkd_form = unicodedata.normalize('NFKD', name)
    ascii_only = nfkd_form.encode('ASCII', 'ignore').decode('utf-8')
    return re.sub(r'[^a-zA-Z0-9]', '', ascii_only).lower()

def generate_personal_email(first, last):
    return f"{sanitize_name(first)}.{sanitize_name(last)}@example.com"

def get_next_versioned_filename(prefix="generated_employees", ext=".csv"):
    version = 2
    while os.path.exists(f"{prefix}_v{version}{ext}"):
        version += 1
    return f"{prefix}_v{version}{ext}", version

# Initialize records
records = []
managers = {}
id_counter = 1000

# Create CEO
ceo_country = random.choice(list(faker_locales.keys()))
faker_ceo = Faker(faker_locales[ceo_country])
ceo_first = faker_ceo.first_name()
ceo_last = faker_ceo.last_name()
ceo_start_date = random_date(datetime(2019, 1, 1), datetime(2020, 12, 31))

ceo = {
    "nationalID": str(id_counter),
    "firstName": ceo_first,
    "middleName": "",
    "lastName": ceo_last,
    "birthDate": random_date(datetime(1975, 1, 1), datetime(2006, 12, 31)),
    "department": "Executive",
    "jobTitle": "CEO",
    "manager": "",
    "startDate": ceo_start_date,
    "terminationDate": "",
    "country": ceo_country,
    "personalMail": generate_personal_email(ceo_first, ceo_last),
    "phoneNumber": generate_phone_number(country_codes[ceo_country])
}
records.append(ceo)
id_counter += 1

# Create Leads/Managers
for dept, roles in departments_jobs.items():
    if dept == "Executive":
        continue
    lead_role = next((r for r in roles if "Lead" in r or "Manager" in r), None)
    if lead_role:
        country = random.choice(list(faker_locales.keys()))
        faker_local = Faker(faker_locales[country])
        first = faker_local.first_name()
        last = faker_local.last_name()
        lead_start = random_date(datetime.strptime(ceo_start_date, "%d/%m/%Y"), datetime(2025, 4, 16))
        record = {
            "nationalID": str(id_counter),
            "firstName": first,
            "middleName": "",
            "lastName": last,
            "birthDate": random_date(datetime(1975, 1, 1), datetime(2006, 12, 31)),
            "department": dept,
            "jobTitle": lead_role,
            "manager": f"{ceo_first} {ceo_last}",
            "startDate": lead_start,
            "terminationDate": "" if random.random() < 0.8 else "01/01/2026",
            "country": country,
            "personalMail": generate_personal_email(first, last),
            "phoneNumber": generate_phone_number(country_codes[country])
        }
        records.append(record)
        managers[dept] = f"{first} {last}"
        id_counter += 1

# Generate remaining employees
while len(records) < 50:
    dept = random.choice([d for d in departments_jobs if d != "Executive"])
    roles = [r for r in departments_jobs[dept] if "Lead" not in r and "Manager" not in r]
    job = random.choice(roles)
    country = random.choice(list(faker_locales.keys()))
    faker_local = Faker(faker_locales[country])
    first = faker_local.first_name()
    last = faker_local.last_name()
    start_date = random_date(datetime.strptime(ceo_start_date, "%d/%m/%Y"), datetime(2025, 4, 16))
    record = {
        "nationalID": str(id_counter),
        "firstName": first,
        "middleName": "",
        "lastName": last,
        "birthDate": random_date(datetime(1975, 1, 1), datetime(2006, 12, 31)),
        "department": dept,
        "jobTitle": job,
        "manager": managers.get(dept, ""),
        "startDate": start_date,
        "terminationDate": "" if random.random() < 0.8 else "01/01/2026",
        "country": country,
        "personalMail": generate_personal_email(first, last),
        "phoneNumber": generate_phone_number(country_codes[country])
    }
    records.append(record)
    id_counter += 1

# Prepare CSV
csv_headers = ["nationalID", "firstName", "middleName", "lastName", "birthDate", "department", "jobTitle",
               "manager", "startDate", "terminationDate", "personalMail", "phoneNumber", "country"]

filename, version = get_next_versioned_filename()

with open(filename, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
    writer.writeheader()
    for r in records:
        writer.writerow(r)

print(f"✅ CSV file '{filename}' (version v{version}) has been created successfully.")
