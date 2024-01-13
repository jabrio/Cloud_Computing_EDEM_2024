""" 
Script: Write files to a GCP Bucket from a local file

Description: This script gives an example of how to store a CSV file into a GCP bucket from a local file and then it prints its content into a Pandas DF

EDEM. Master Data Analytics 2023/2024
Weekday Group Professor: Miguel Moratilla
Weekend Group Professor: Javi Briones
"""

import pandas as pd
from google.cloud import storage


def bucket_exists(bucket_name):
    """Determines whether or not a bucket exists."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()

    try:
        storage_client.get_bucket(bucket_name)
        return True
    except:
        return False

def create_bucket(bucket_name):
    """Creates a new bucket."""
    # bucket_name = "your-new-bucket-name"

    storage_client = storage.Client()

    bucket = storage_client.create_bucket(bucket_name)

    print("Bucket {} created".format(bucket.name))

def read_local_csv(file_name):
    df = pd.read_csv(file_name)
    return df

def write_to_gcs(pd_df, bucket_name, blob_name):
    """Write and read a blob from GCS using file-like IO"""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your new GCS object
    # blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Mode can be specified as wb/rb for bytes mode.
    # See: https://docs.python.org/3/library/io.html
    with blob.open("w") as f:
        pd_df.to_csv(f, index=False)

    with blob.open("r") as f:
        df = pd.read_csv(f)
        print(df.head())



if __name__ == "__main__":

    local_file_name = "./data/employee_data_write.csv"
    bucket_name = "data-ejercicio-2-write"
    blob_name = "employee_data_write.csv"

    if not bucket_exists(bucket_name):
        create_bucket(bucket_name)

    pd_df = read_local_csv(local_file_name)
    write_to_gcs(pd_df, bucket_name, blob_name)