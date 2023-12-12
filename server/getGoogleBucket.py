import os
import pandas as pd
from google.cloud import storage
from google.cloud.bigquery.client import Client

def getData(fileName):
    # os.environ['REQUESTS_CA_BUNDLE'] = './cacert.pem'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './winter-wonder-402117-38e43710a6f1.json'
    bq_client = Client()

    bucket_name = fileName
    file_path = fileName + '.csv'

    # Initialize a client to interact with Google Cloud Storage
    client = storage.Client()

    # Get the specified bucket
    bucket = client.bucket(bucket_name)

    blob = bucket.blob(file_path)

    # Download the CSV file to a local temporary file
    temp_local_file = "/tmp/temp_csv_file.csv"
    blob.download_to_filename(temp_local_file)

    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(temp_local_file)

    return df