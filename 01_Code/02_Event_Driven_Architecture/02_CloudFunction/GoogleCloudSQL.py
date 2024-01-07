""" 
Script: Google Cloud SQL Utils

Description: Python class to group methods related to Cloud SQL.

EDEM. Master Data Analytics 2023/2024
Weekday Group Professor: Miguel Moratilla
Weekend Group Professor: Javi Briones
"""

#Import libraries
from google.cloud.sql.connector import Connector, IPTypes
import os

class GoogleCloudSSQL:
    
    """ Google Cloud SQL Operations """

    def __init__(self):

        """ Initialize the attributes of the class.
        Params:
            We will gather all the arguments from the environment variables
            declared when creating the function.
        Returns:
            -
        """
        
        self.pg_instance_url = os.getenv("PG_INSTANCE_URL")
        self.db_user = os.getenv("DB_USER")
        self.db_psw = os.getenv("DB_PASSWORD")
        self.pg_database = os.getenv("PG_DB")

    def getPGconn(self):

        """Google Cloud SQL Database connection.
        Returns:
            conn (pg8000.dbapi.Connection): Connection object instantiated.
        """
        
        with Connector() as connector:
            conn = connector.connect(
                self.pg_instance_url,
                "pg8000",
                user=self.db_user,
                password=self.db_psw,
                db=self.pg_database,
                ip_type= IPTypes.PUBLIC
            )
        return conn