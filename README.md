# random-csv-generator
This is a random Identity generator in CSV format for IGA tools. 

- The CSV file will include this headers initially : **nationalID,firstName,middleName,lastName,birthDate,department,jobTitle,manager,startDate,terminationDate,personalMail,phoneNumber,country**

You can adjust the headers from this part of the code:

```python
# Prepare CSV
csv_headers = ["nationalID", "firstName", "middleName", "lastName", "birthDate", "department", "jobTitle",
               "manager", "startDate", "terminationDate", "personalMail", "phoneNumber", "country"]
```

Increment/decrement the user records by modifying the number in this line :

```python
# Generate remaining employees
while len(records) < 50:
```
