""" 
Script: Post content in an API deployed in Cloud Run

Description: This script gives an example of how make post request to an API deployed in Cloud Run

EDEM. Master Data Analytics 2023/2024
Weekday Group Professor: Miguel Moratilla
Weekend Group Professor: Javi Briones
"""

from faker import Faker
import random
import requests
import logging

fake = Faker()

url = "https://my-python-api-oxdx2hzcbq-no.a.run.app/employees"

def generate_employee():
    employee_id = fake.unique.random_int(min=1000, max=10000)
    return {
        "id": employee_id,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "salary": round(random.uniform(30000, 100000), 2)
    }

# Loop to send data for 100 employees
if __name__ == "__main__":

    # Set Logs
    logging.getLogger().setLevel(logging.INFO)

    employees = 10

    for _ in range(employees):
        employee = generate_employee()
        post_response = requests.post(url, json=employee)
        if post_response.status_code != 201:
            logging.info(f"Failed to add employee: {employee}")
        else:
            logging.info(f"Employee added: {employee}")
