import pandas as pd
import boto3
from botocore.exceptions import ClientError
from io import StringIO  # Import StringIO

def bucket_exists(s3_client, bucket_name):
    """Determines whether or not a bucket exists in AWS S3."""
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        return True
    except ClientError:
        return False

def create_bucket(s3_client, bucket_name, region=None):
    """Creates a new bucket in AWS S3."""
    try:
        if region is None:
            # Specify the default region or the region you are working with
            region = 'us-east-1'
        location = {'LocationConstraint': region}
        s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        print("Bucket {} created".format(bucket_name))
    except ClientError as e:
        print(e)

def read_local_csv(file_name):
    df = pd.read_csv(file_name)
    return df

def write_to_s3(pd_df, bucket_name, object_name, region=None):
    """Write a DataFrame to a CSV in S3."""
    csv_buffer = StringIO()  # Now StringIO is defined
    pd_df.to_csv(csv_buffer, index=False)
    
    s3_resource = boto3.resource('s3', region_name=region)
    s3_resource.Object(bucket_name, object_name).put(Body=csv_buffer.getvalue())

    print(f'{object_name} written to bucket {bucket_name}')

if __name__ == "__main__":
    s3_client = boto3.client('s3')

    local_file_name = "./employee_data_write.csv"
    bucket_name = "ejercicio-2-write"
    object_name = "employee_data_write.csv"
    region = 'eu-north-1'  # Specify your region here

    if not bucket_exists(s3_client, bucket_name):
        create_bucket(s3_client, bucket_name, region)

    pd_df = read_local_csv(local_file_name)
    write_to_s3(pd_df, bucket_name, object_name, region)
