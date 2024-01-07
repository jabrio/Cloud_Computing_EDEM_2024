from flask import Flask, jsonify, request
from faker import Faker
import random

app = Flask(__name__)
fake = Faker()

# Function to generate fake employee data
def generate_employee_data(n):
    employees = {}
    for _ in range(n):
        employee_id = fake.unique.random_int(min=1, max=1000)
        employees[employee_id] = {
            "id": employee_id,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "salary": round(random.uniform(30000, 100000), 2)
        }
    return employees

# Generate 100 employees
employees = generate_employee_data(100)

@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.json
    employee_id = data.get('id')
    if employee_id is None or employee_id in employees:
        return jsonify({"error": "Invalid or duplicate employee ID"}), 400
    employees[employee_id] = data
    return jsonify(data), 201

@app.route('/employees', methods=['GET'])
def get_all_employees():
    return jsonify(list(employees.values()))

@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    employee = employees.get(employee_id)
    if employee:
        return jsonify(employee)
    return 'Employee not found', 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

