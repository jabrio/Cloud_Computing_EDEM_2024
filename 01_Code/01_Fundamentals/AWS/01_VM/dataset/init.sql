CREATE TABLE IF NOT EXISTS employees_data (
    employee_id INT NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    salary DECIMAL(10,2) NOT NULL
);

COPY employees_data
FROM '/docker-entrypoint-initdb.d/employees.csv'
DELIMITER ','
CSV HEADER;

