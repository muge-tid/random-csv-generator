import csv
import os 
# Read the identity CSV and extract unique departments
input_file = 'generated_employees_v3.csv'  # replace it with the file name
departments = set()

with open(input_file, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        department = row['department'].strip()
        if department:  # skip empty values
            departments.add(department)

def get_next_versioned_filename(prefix="generated_departments", ext=".csv"):
    version = 1
    while os.path.exists(f"{prefix}_v{version}{ext}"):
        version += 1
    return f"{prefix}_v{version}{ext}", version

# Write the new CSV with name and description
filename, version = get_next_versioned_filename()

with open(filename,'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['name', 'description'])  # headers
    for dept in sorted(departments):
        writer.writerow([dept, f"{dept} identity group"])

print(f"✅ CSV file '{filename}' (version v{version}) has been created successfully.")