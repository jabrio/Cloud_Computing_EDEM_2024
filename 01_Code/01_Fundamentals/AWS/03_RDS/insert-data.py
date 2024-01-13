""" 
Script: Run queries in a Postgres instance of AWS RDS service

Description: This script gives an example of how run SQL queries into a Postgres instance deployed in AWS RDS 

EDEM. Master Data Analytics 2023/2024
Weekday Group Professor: Miguel Moratilla
Weekend Group Professor: Javi Briones
"""

import os
import csv
import logging
import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError, SQLAlchemyError
from dotenv import load_dotenv

load_dotenv()

def create_engine_rds() -> sqlalchemy.engine.base.Engine:
    """
    Initializes a connection pool for an AWS RDS instance of Postgres.
    """
    db_user = os.environ["DB_USER"]  # e.g. 'my-db-user'
    db_pass = os.environ["DB_PASS"]  # e.g. 'my-db-password'
    db_host = os.environ["DB_HOST"]  # e.g. 'my-db-instance.123456789012.us-west-2.rds.amazonaws.com'
    db_name = os.environ["DB_NAME"]  # e.g. 'my-database'
    db_port = os.environ.get("DB_PORT", "5432")  # default port for PostgreSQL

    # SQLAlchemy engine for PostgreSQL
    engine = create_engine(f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}')

    return engine

def create_schema_and_table(engine, schema_name, table_name):
    """
    Create a new schema and table if they don't exist.
    """
    try:
        with engine.connect() as conn:
            trans = conn.begin()
            # Create Schema
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name};"))
            logging.info(f"Schema '{schema_name}' checked/created.")

            # Create Table
            create_table_query = text(f"""
                CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (
                    id INT NULL,
                    first_name VARCHAR(45) NULL,
                    last_name VARCHAR(45) NULL,
                    email VARCHAR(45) NULL,
                    salary NUMERIC(10,2) NULL
                );
            """)
            conn.execute(create_table_query)
            logging.info(f"Table '{table_name}' in schema '{schema_name}' checked/created.")

            trans.commit()
    except SQLAlchemyError as e:
        logging.error(f"Error creating schema/table: {e}")
        raise

def insert_data(conn, schema_name, table_name, row):
    """
    Insert a single row into the database.
    """
    insert_query = text(f"""
    INSERT INTO {schema_name}.{table_name} (id, first_name, last_name, email, salary) VALUES (:id, :first_name, :last_name, :email, :salary)
    """)
    try:
        with engine.connect() as conn:
            trans = conn.begin()
            conn.execute(insert_query, {"id": row[0], "first_name": row[1], "last_name": row[2], "email": row[3], "salary": row[4]})
            trans.commit()
            logging.info(f"Inserting data row: {row}")
    except SQLAlchemyError as e:
        logging.error(f"Error inserting data: {e}")
        raise

if __name__ == "__main__":
    # Set Logs
    logging.basicConfig(level=logging.INFO)

    engine = create_engine_rds()

    # Define your schema and table names here
    schema_name = "my_custom_schema"
    table_name = "employee"

    # Create schema and table
    create_schema_and_table(engine, schema_name, table_name)

    # Insert data
    with engine.connect() as conn:
        with open('./data/employees_ej3_python.csv', 'r') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)  # Skip header row, if your CSV has one
            for row in csv_reader:
                # Convert id and salary to appropriate types
                row[0] = int(row[0]) if row[0] else None  # Convert id to int, handle empty values
                row[4] = float(row[4]) if row[4] else None  # Convert salary to float, handle empty values
                insert_data(conn, schema_name, table_name, row)
        logging.info("Data insertion completed")
