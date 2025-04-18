# random-csv-generator
This is a random Identity generator in CSV format for IGA tools. 

- The CSV file will include this headers initially : **nationalID,firstName,middleName,lastName,birthDate,department,jobTitle,manager,startDate,terminationDate,personalMail,phoneNumber,country**

##  Adjust Headers 
You can adjust the headers from this part of the code:
```python
# Prepare CSV
csv_headers = ["nationalID", "firstName", "middleName", "lastName", "birthDate", "department", "jobTitle",
               "manager", "startDate", "terminationDate", "personalMail", "phoneNumber", "country"]
```
Keep in mind you also have to modify the header mappings. 

## startDate Generation

Date attributes (birthDate, startDate, terminationDate) is configured in the below function.

``` python
def random_date(start, end, date_format="%d/%m/%Y"):
    delta = end - start
    return (start + timedelta(days=random.randint(0, delta.days))).strftime(date_format)
```
If you want to modify date ranges, please modify the function call. Example below demonstrates a date between CEO's start date and 16/04/2025 for `startDate` attribute.

```python
start_date = random_date(datetime.strptime(ceo_start_date, "%d/%m/%Y"), datetime(2025, 4, 16))
```

## Modifying the Record Number

If you want to generate more or less records please modify the number in below code: 

```python
# Generate remaining employees
while len(records) < 50:
```
