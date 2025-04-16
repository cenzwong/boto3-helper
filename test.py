import boto3
from botoo import list_files_in_s3_path

s3_client = boto3.client('s3')
files = list_files_in_s3_path(s3_client, 'uk-fuel-price-data', "raw")
print(files)