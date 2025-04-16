import boto3
from typing import List

def get_data(s3_client: 'boto3.client', bucket_name: str, file_key: str) -> str:
    """Fetches data from an S3 bucket and returns it as a decoded string.

    Args:
        s3_client (boto3.client): The S3 client used to interact with the S3 service.
        bucket_name (str): The name of the S3 bucket.
        file_key (str): The key (path) of the file within the S3 bucket.

    Returns:
        str: The content of the file as a decoded string.
    """
    # Get the object from the specified S3 bucket and file key
    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    
    # Read the content of the file and decode it to a UTF-8 string
    return response["Body"].read().decode("utf-8")


def upload_file_to_s3(s3_client: 'boto3.client', file_path: str, bucket_name: str, file_key: str) -> None:
    """Uploads a file to an S3 bucket.

    Args:
        s3_client (boto3.client): The S3 client used to interact with the S3 service.
        file_path (str): The local path to the file to be uploaded.
        bucket_name (str): The name of the S3 bucket.
        file_key (str): The key (path) where the file will be stored in the S3 bucket.

    Returns:
        None
    """
    # Upload the file to the specified S3 bucket and file key
    s3_client.upload_file(file_path, bucket_name, file_key)

def list_files_in_s3_path(s3_client: 'boto3.client', bucket_name: str, prefix: str = '') -> List[str]:
    """Lists all files in a specified path within an S3 bucket, excluding folders.

    Args:
        s3_client (boto3.client): The S3 client used to interact with the S3 service.
        bucket_name (str): The name of the S3 bucket.
        prefix (str, optional): The prefix (path) within the S3 bucket to list files. Defaults to ''.

    Returns:
        List[str]: A list of file keys (paths) in the specified path within the S3 bucket, excluding folders.
    """
    # List objects in the specified S3 bucket and prefix
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    
    # Extract the file keys from the response, excluding folders
    file_keys = [item['Key'] for item in response.get('Contents', []) if not item['Key'].endswith('/')]
    
    return file_keys


