""" 
Script: Google Cloud Function Code

Description: This 2Gen Cloud Function will be triggered by a change in our storage bucket.

EDEM. Master Data Analytics 2023/2024
Weekday Group Professor: Miguel Moratilla
Weekend Group Professor: Javi Briones
"""

# Import Python Libraries
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, VARCHAR, INTEGER, DOUBLE_PRECISION
from sqlalchemy import create_engine
import functions_framework
import pandas as pd
import logging
import ast
import io
import os

# Custom Methods
from GoogleCloudStorage import GoogleCloudStorage
from GoogleCloudSQL import GoogleCloudSSQL

# Set Logs
logging.getLogger().setLevel(logging.INFO)

""" Dtypes """
customer_dtype = {
    'customer_id': UUID,
    'customer_name': VARCHAR,
    'customer_email': VARCHAR,
    'store_id': VARCHAR
}

purchase_details_dtype = {
    "purchase_detail_id": INTEGER,
    "purchase_id": VARCHAR,
    "product_id": VARCHAR,
    "quantity": INTEGER
}

product_dtype = {
    'product_id': VARCHAR,
    'product_name': VARCHAR,
    'category': VARCHAR,
    "price": DOUBLE_PRECISION
}

purchase_dtype = {
    'purchase_id': VARCHAR,
    'customer_id': UUID,
    'purchase_date': TIMESTAMP,
    'total_amount': DOUBLE_PRECISION,
    'payment_method':VARCHAR
}

""" Helpful Methods """

def prepare_dataframe_for_insert(df, column_list: list, event: str):

    """ Transform a Pandas DataFrame as input into the columns required by the SQL table.
    Params:
        df (pandas.core.frame.DataFrame): pandas DataFrame that we just read from the GCS bucket.
        column_list (list):List of columns that we want the DataFrame to include or remove,
            depending on the event we pass as a parameter.
        event (str): (Create or Drop) Depending on the operation to be performed.
    Returns:
        (pandas.core.frame.DataFrame): The resulting DataFrame after the requested transformations.
    """

    if event == 'Create':
        return df[column_list]
    
    if event == 'Drop':
        dropped_df = df.drop(column_list, axis=1)
        return dropped_df.reset_index(drop=True)

def insert_dataframe_into_sql(df, table_name, dtype, pool):

    """ Store Pandas DataFrames into SQL tables.
    Params:
        df (pandas.core.frame.DataFrame): Pandas Dataframe we want to store into SQL tables.
        table_name (str): Name of the table where we want to store the data.
        dtype (dict): Dict specifying the mapping between each field in the DataFrame
            and its format in the SQL table.
        pool (sqlalchemy '_engine.Engine'): SQLAlchemy engine to connect to the SQL instance.
    Returns:
        -
    """

    return df.to_sql(table_name, con=pool, if_exists='append', index=False, schema='public', dtype=dtype)

def explode_items_column(df, column_list: list, column_name: str):

    """ Transform each element of a list-like to a row, replicating index values.
    Params:
        df (pandas.core.frame.DataFrame): Pandas DataFrame that we want to transform.
        column_list (list): List of fields resulting from the explode operation.
        column_name (str): Column name that we want to explode into different rows with the same index.
    Returns:
        (pandas.core.frame.DataFrame): The resulting DataFrame after the requested transformations.
    """

    exploded_df = df.explode(column_name)
    exploded_df[column_list] = pd.DataFrame(exploded_df[column_name].tolist(), index=exploded_df.index)
    
    return exploded_df

# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def store_data_into_cloud_sql(cloud_event):

    """ Triggered by a change to a Cloud Storage bucket.
    Args:
        CloudEvents: Payload and metadata related to the event.
        More info: https://cloud.google.com/functions/docs/writing/write-event-driven-functions
    Returns:
        -
    Raises:
        Exception: if there is an error processing or saving the data to Cloud SQL using Pandas.
    """
    
    # Dealing with the event
    data = cloud_event.data

    bucket_name = data["bucket"]
    file_name = data["name"]

    logging.info(f"New event registered: {file_name} has been stored in {bucket_name}.")

    # Read CSV from our Google Cloud Storage Bucket
    gcs_class = GoogleCloudStorage(project_id=os.getenv('PROJECT_ID'), bucket_name=bucket_name)
    csv = gcs_class.readCSVFromGCS(file_name=file_name)
    
    df = pd.read_csv(io.BytesIO(csv), sep=',')

    # Map str as a list
    df['items'] = df['items'].apply(ast.literal_eval)
    
    # Preparing data to be inserted into the Cloud SQL tables.
    try:
        sql_class = GoogleCloudSSQL()
        pool = create_engine("postgresql+pg8000://", creator=sql_class.getPGconn)

        """ Customers Table """
        customer_df = prepare_dataframe_for_insert(df, 
            column_list=['customer_id', 'customer_name','customer_email','store_id'], event='Create')

        insert_dataframe_into_sql(
            df=customer_df, table_name='customers',dtype=customer_dtype, pool=pool)

        logging.info("Customers inserted successfully")

        """ Products Table """
        product_purchase_df = prepare_dataframe_for_insert(df, 
            column_list=['purchase_id','items'], event='Create')

        product_purchase_expanded_df = explode_items_column(df=product_purchase_df,
            column_list=['product_id', 'product_name', 'category', 'quantity', 'price'], column_name='items')

        products_df = prepare_dataframe_for_insert(df=product_purchase_expanded_df, 
            column_list=['items','quantity','purchase_id'], event='Drop')

        insert_dataframe_into_sql(
            df=products_df, table_name='products',dtype=product_dtype, pool=pool)

        logging.info("Products inserted successfully")

        """ Purchases Table """
        purchases_df = prepare_dataframe_for_insert(df, 
            column_list=['purchase_id','customer_id','purchase_date','total_amount','payment_method'], event='Create')

        insert_dataframe_into_sql(
            df=purchases_df, table_name='purchases',dtype=purchase_dtype, pool=pool)

        logging.info("Purchases inserted successfully")

        """ Purchase Details Table """
        purchase_details_df = prepare_dataframe_for_insert(df=product_purchase_expanded_df, 
            column_list=['items','product_name','price','category'], event='Drop')

        insert_dataframe_into_sql(
            df=purchase_details_df, table_name='purchasedetails', dtype=purchase_details_dtype, pool=pool)

        logging.info("Purchase Details inserted successfully")
        
        return logging.info("The data has been successfully inserted into the Cloud SQL tables")

    except Exception as err:

        return logging.error(f"Error while trying to insert data into Cloud SQL: {err}")

    finally:

        gcs_class.__exit__()