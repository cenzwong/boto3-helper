import pytest
from unittest.mock import MagicMock
from botocore.exceptions import NoCredentialsError, ClientError

# Fixtures
@pytest.fixture
def s3_client():
    return MagicMock()

@pytest.fixture
def bucket_name():
    return "test-bucket"

@pytest.fixture
def file_key():
    return "test-file.txt"

@pytest.fixture
def file_path():
    return "/path/to/test-file.txt"

# Test cases for get_data
def test_get_data_success(s3_client, bucket_name, file_key):
    from botoo.s3 import get_data
    s3_client.get_object.return_value = {"Body": MagicMock(read=lambda: b"test content")}
    result = get_data(s3_client, bucket_name, file_key)
    assert result == "test content"

def test_get_data_no_credentials(s3_client, bucket_name, file_key):
    from botoo.s3 import get_data
    s3_client.get_object.side_effect = NoCredentialsError
    with pytest.raises(NoCredentialsError):
        get_data(s3_client, bucket_name, file_key)

def test_get_data_client_error(s3_client, bucket_name, file_key):
    from botoo.s3 import get_data
    s3_client.get_object.side_effect = ClientError({"Error": {"Code": "404", "Message": "Not Found"}}, "get_object")
    with pytest.raises(ClientError):
        get_data(s3_client, bucket_name, file_key)

# Test cases for upload_file_to_s3
def test_upload_file_to_s3_success(s3_client, file_path, bucket_name, file_key):
    from botoo.s3 import upload_file_to_s3
    upload_file_to_s3(s3_client, file_path, bucket_name, file_key)
    s3_client.upload_file.assert_called_once_with(file_path, bucket_name, file_key)

def test_upload_file_to_s3_no_credentials(s3_client, file_path, bucket_name, file_key):
    from botoo.s3 import upload_file_to_s3
    s3_client.upload_file.side_effect = NoCredentialsError
    with pytest.raises(NoCredentialsError):
        upload_file_to_s3(s3_client, file_path, bucket_name, file_key)

def test_upload_file_to_s3_client_error(s3_client, file_path, bucket_name, file_key):
    from botoo.s3 import upload_file_to_s3
    s3_client.upload_file.side_effect = ClientError({"Error": {"Code": "403", "Message": "Forbidden"}}, "upload_file")
    with pytest.raises(ClientError):
        upload_file_to_s3(s3_client, file_path, bucket_name, file_key)

# Test cases for list_files_in_s3_path
def test_list_files_in_s3_path_success(s3_client, bucket_name):
    from botoo.s3 import list_files_in_s3_path
    s3_client.list_objects_v2.return_value = {"Contents": [{"Key": "file1.txt"}, {"Key": "file2.txt"}]}
    result = list_files_in_s3_path(s3_client, bucket_name)
    assert result == ["file1.txt", "file2.txt"]

def test_list_files_in_s3_path_empty(s3_client, bucket_name):
    from botoo.s3 import list_files_in_s3_path
    s3_client.list_objects_v2.return_value = {"Contents": []}
    result = list_files_in_s3_path(s3_client, bucket_name)
    assert result == []

def test_list_files_in_s3_path_no_credentials(s3_client, bucket_name):
    from botoo.s3 import list_files_in_s3_path
    s3_client.list_objects_v2.side_effect = NoCredentialsError
    with pytest.raises(NoCredentialsError):
        list_files_in_s3_path(s3_client, bucket_name)

def test_list_files_in_s3_path_client_error(s3_client, bucket_name):
    from botoo.s3 import list_files_in_s3_path
    s3_client.list_objects_v2.side_effect = ClientError({"Error": {"Code": "403", "Message": "Forbidden"}}, "list_objects_v2")
    with pytest.raises(ClientError):
        list_files_in_s3_path(s3_client, bucket_name)
