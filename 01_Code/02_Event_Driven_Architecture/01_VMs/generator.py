""" 
Script: Data Stream Generator

Description: The script will simulate the transactions that may occur in a conventional grocery store.

EDEM. Master Data Analytics 2023/2024
Weekday Group Professor: Miguel Moratilla
Weekend Group Professor: Javi Briones
"""

#Import libraries
from google.cloud import storage
from datetime import datetime
from faker import Faker
import pandas as pd
import argparse
import logging
import secrets
import string
import random
import uuid
import time
import os

fake = Faker()

#Input arguments
parser = argparse.ArgumentParser(description=('Grocery Store Data Generator.'))
parser.add_argument(
                '--project_id',
                required=True,
                help='Google Cloud Project ID.')

parser.add_argument(
                '--bucket_name',
                required=True,
                help='Google CLoud Storage Bucket Name.')

parser.add_argument(
                '--store_id',
                required=True,
                help='Grocery Store ID.')

args, opts = parser.parse_known_args()

class GoogleCloudStorage:
    
    """ Store the data into the Google Cloud Storage Bucket """

    def __init__(self, project_id: str, bucket_name: str):

        """ Initialize the attributes of the class.
        Params:
            project_id (str): Google Cloud Project ID.
            bucket_name (str): Google Cloud Storage Bucket Name.
        """
        
        self.client = storage.Client(project=project_id)
        self.project_id = project_id
        self.bucket_name = bucket_name

    def writeCSVToGCS(self, df, bucket_folder: str, file_name: str):

        """ Write CSVs into the Google Cloud Storage Bucket.
        Params:
            df (pandas.core.frame.DataFrame): Pandas Dataframe to be stored into the GCS Bucket.
            bucket_folder (str): Folder where we will store the CSV within the bucket (Optional).
            file_name (str): File name that we will upload to the bucket.
        """

        bucket = self.client.get_bucket(self.bucket_name)

        if bucket_folder != None:
            blob = bucket.blob(os.path.join(bucket_folder,file_name))
        else:
            blob = bucket.blob(file_name)

        blob.upload_from_string(df.to_csv(index=False,sep=',',encoding='utf-8'), 'text/csv')

        return "New data dump completed successfully."

    def __exit__(self):

        self.client.close()
        logging.info("Google Cloud Storage Client closed.")



fake = Faker()
            
""" Helpful methods """

def generateMockProducts(num_products=random.randint(1, 20)):
    
    """ Generate random products for each purchase.
    Params:
        num_products (int): Number of products per purchase.
    Returns:
        products (list(dict)): List of products for each purchase.
    """
    
    products = []

    for _ in range(num_products):

        product = {
            "product_id": ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(6)),
            "product_name": fake.word(),
            "category": random.choice(["Groceries", "Seafood", "Bakery", "Beverages", "Personal Care"]),
            "quantity": random.randint(1, 10),
            "price": round(random.uniform(0.5, 25), 2),
        }

        # Append product dict to the list
        products.append(product)

    return products


def generateMockData():

    """ Generate mock data simulating grocery store purchases.
    Params:
        -
    Returns:
        purchase_details (dict): Purchase data.
    """

    # Generate random products for each purchase
    products = generateMockProducts()

    # Purchase Details
    purchase_details = {
        "store_id": args.store_id,
        "customer_id": str(uuid.uuid4()),
        "customer_name": fake.name(),
        "customer_email": fake.email(),
        "purchase_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": products,
        "total_amount": sum(product["price"] * product["quantity"] for product in products),
        "payment_method": random.choice(["Credit Card", "Debit Card", "Cash"]),
        "purchase_id": ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(10))
    }

    logging.info("New transaction completed: %s", purchase_details)

    return purchase_details

""" Generator Code """

def run_generator(project_id: str, bucket_name: str):

    """ Main method for running the generator.
    Params:
        project_id (str): Google Cloud Project ID.
        bucket_name (str): Google Cloud Storage Bucket Name.
    Raises:
        Exception: If there is an issue generating the CSV 
        or inserting it into the GCS bucket.
    """

    shopping_list = []
    
    try:

        # Instantiate Google Cloud Storage Python Class
        bucket_class = GoogleCloudStorage(project_id, bucket_name)
        
        for _ in range(random.randint(5, 15)):
        
            # Simulate data dumps that a Grocery Store might perform
            simulated_purchase = generateMockData()

            time.sleep(1)

            shopping_list.append(simulated_purchase)

        # Create a Pandas DataFrame with the combined data
        df = pd.DataFrame(shopping_list)

        # Save CSV to the GCS bucket
        bucket_class.writeCSVToGCS(
            df, bucket_folder=args.store_id,
            file_name=f'{args.store_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
            
    except Exception as err:
        logging.error("Error while inserting data into the GCS Bucket: %s", err)
    
    finally:
        bucket_class.__exit__()

if __name__ == "__main__":
    
    # Set Logs
    logging.getLogger().setLevel(logging.INFO)
    
    # Run Generator
    while True:
        run_generator(args.project_id, args.bucket_name)