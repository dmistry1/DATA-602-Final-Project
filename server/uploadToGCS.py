import os
from google.cloud import storage
from google.cloud.bigquery.client import Client
import pandas as pd

def upload_csv_to_gcs(bucket_name, file_name, df):
# Create a storage client
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './winter-wonder-402117-38e43710a6f1.json'
    bq_client = Client()
    client = storage.Client()

    # Get the bucket and blob
    bucket = client.get_bucket(bucket_name)
    blob = storage.Blob(file_name, bucket)

    # Convert the DataFrame to CSV format
    updated_csv_data = df.to_csv(index=False)

    # Upload the updated CSV data back to Google Cloud Storage
    blob.upload_from_string(updated_csv_data, content_type='text/csv')

    print(f"Data updated and file uploaded to Google Cloud Storage: {file_name}")
