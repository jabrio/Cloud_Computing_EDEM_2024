""" 
Script: Get files from a S3 AWS Bucket

Description: This script gives an example of how to extract files from a Bucket in AWS and print the content in a Pandas DF

EDEM. Master Data Analytics 2023/2024
Weekday Group Professor: Miguel Moratilla
Weekend Group Professor: Javi Briones
"""

import pandas as pd
import boto3
from io import StringIO

def read_s3(bucket_name, object_name):
    """Read an object from S3 and return it as a pandas DataFrame."""
    # Create an S3 client
    s3_client = boto3.client('s3')

    # Get the object from the bucket
    csv_obj = s3_client.get_object(Bucket=bucket_name, Key=object_name)
    body = csv_obj['Body']

    # Read the body into a string
    csv_string = body.read().decode('utf-8')

    # Use pandas to read the CSV string
    df = pd.read_csv(StringIO(csv_string))
    print(df.head())

if __name__ == "__main__":
    read_s3("ejercicio-2", "02_S3/data/employee_data.csv")
