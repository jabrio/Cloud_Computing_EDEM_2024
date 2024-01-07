""" 
Script: Google Cloud Storage Operations

Description: Python class to group methods related to Cloud Storage.

EDEM. Master Data Analytics 2023/2024
Weekday Group Professor: Miguel Moratilla
Weekend Group Professor: Javi Briones
"""

#Import libraries
from google.cloud import storage
import logging

class GoogleCloudStorage:
    
    """ Google Cloud Storage Operations """

    def __init__(self, project_id: str, bucket_name: str):

        """ Initialize the attributes of the class.
        Params:
            project_id (str): Google Cloud Project ID.
            bucket_name (str): Google Cloud Storage Bucket Name.
        Returns:
            -
        """
        
        self.client = storage.Client()
        self.project_id = project_id
        self.bucket_name = bucket_name

    def readCSVFromGCS(self, file_name: str):

        """ Read CSVs from a Google Cloud Storage Bucket.
        Params:
            file_name (str): Name of the file we want to read.
        Returns:
            df (str): Pandas DataFrame returned as a blob string format.
        """

        blob = self.client.get_bucket(self.bucket_name).blob(file_name)

        return blob.download_as_string()

    def __exit__(self):

        self.client.close()
        logging.info("Google Cloud Storage Client closed.")