""" 
Script: Insert rows in a table stored in a Database in Cloud SQL

Description: This script gives an example of how to load the content of a CSV file into rows of a database inside a Postgres instance in Cloud SQL

EDEM. Master Data Analytics 2023/2024
Weekday Group Professor: Miguel Moratilla
Weekend Group Professor: Javi Briones
"""

import os
import csv
import logging

from google.cloud.sql.connector import Connector, IPTypes
import pg8000

import sqlalchemy
from sqlalchemy import text



from dotenv import load_dotenv
load_dotenv()

def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of Postgres.

    Uses the Cloud SQL Python Connector package.
    """
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.

    instance_connection_name = os.environ[
        "INSTANCE_CONNECTION_NAME"
    ]  # e.g. 'project:region:instance'
    db_user = os.environ["DB_USER"]  # e.g. 'my-db-user'
    db_pass = os.environ["DB_PASS"]  # e.g. 'my-db-password'
    db_name = os.environ["DB_NAME"]  # e.g. 'my-database'

    ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

    # initialize Cloud SQL Python Connector object
    connector = Connector()

    def getconn() -> pg8000.dbapi.Connection:
        conn: pg8000.dbapi.Connection = connector.connect(
            instance_connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
            ip_type=ip_type,
        )
        return conn
    

    # The Cloud SQL Python Connector can be used with SQLAlchemy
    # using the 'creator' argument to 'create_engine'
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        # ...
    )
    return pool


def insert_data(cursor, row):
    """
    Insert a single row into the database.
    """
    insert_query = """
    INSERT INTO employee (id, first_name, last_name, email, salary) VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, row)
    logging.info("Inserting data row\n")

if __name__ == "__main__":
        # Set Logs
    logging.getLogger().setLevel(logging.INFO)
    pool = connect_with_connector()
    with pool.connect() as conn:
        raw_conn = conn.connection.driver_connection
        cursor = raw_conn.cursor()

        with open('./data/employees_ej3_python.csv', 'r') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)  # Skip header row, if your CSV has one
            for row in csv_reader:
                # Convert id and salary to appropriate types
                row[0] = int(row[0]) if row[0] else None  # Convert id to int, handle empty values
                row[4] = float(row[4]) if row[4] else None  # Convert salary to float, handle empty values
                insert_data(cursor, row)
            raw_conn.commit()
            cursor.close()
        
        logging.info("Data insertion finished")







