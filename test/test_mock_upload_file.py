import pytest
import pytest_mock
import requests_mock
from mcs import BucketAPI, APIClient
from hashlib import md5
from mcs.common import constants as c
import os
import tempfile


def create_temp_file(size, content=None):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        if content is None:
            content = b'\0' * size
        f.write(content)
        temp_file_path = f.name
    return temp_file_path


class TestMockUploadFile:

    @pytest.fixture
    def mock_requests(self):
        with requests_mock.Mocker() as m:
            yield m

    def test_upload_file_success(self, mock_requests, shared_current_time, shared_bucket_list, shared_mock_bucket,
                                 shared_file_list):
        bucket_name = "test-bucket-1"
        object_name = "test-object" + shared_current_time
        file_size = 1024
        temp_file_path = create_temp_file(file_size)

        # Mock API requests
        mock_requests.get(c.BUCKET_LIST, json={'data': shared_bucket_list})
        mock_requests.post(c.CHECK_UPLOAD,
                           json={'status': 'success', 'data': {'file_is_exist': False, 'ipfs_is_exist': False}})
        mock_requests.post(c.UPLOAD_CHUNK, json={"status": "success", "data": ["1_IMG_1710.JPG"]})
        mock_requests.post(c.MERGE_FILE, json={"status": "success",
                                               "data": {"file_id": 12345, "file_hash": "simple_file_hash",
                                                        "file_is_exist": False, "ipfs_is_exist": False, "size": 246493,
                                                        "payload_cid": "simple_payload_cid"}})
        mock_requests.post(c.CREATE_BUCKET, json={'status': 'success', 'data': 'Bucket created successfully'})
        mock_requests.get(c.FILE_INFO, json={"status": "success", "data": {"file_list": shared_file_list}})
        mock_requests.get('https://ipfs.io/ipfs/simple_payload_cid', json={'status': 'success', 'data': 'IPFS is working'})

        bucket_api = shared_mock_bucket
        result = bucket_api.upload_file(bucket_name, object_name, temp_file_path)

        assert result == 'test_file_info'

        os.remove(temp_file_path)

    def test_upload_file_already_exists(self, mock_requests):
        bucket_name = "test-bucket"
        object_name = "test-object"
        bucket_id = "12345"
        file_size = 1024
        temp_file_path = create_temp_file(file_size)

        with open(temp_file_path, 'rb') as file:
            file_hash = md5(file.read()).hexdigest()

        # Mock API requests
        mock_requests.get(f"{API_URL}/get_bucket_id", json={'data': {'bucket_uid': bucket_id}})
        mock_requests.post(f"{API_URL}/check_file", json={'data': {'file_is_exist': True}})

        api_client = APIClient('your_api_key', 'your_access_token', 'your_chain_name')
        bucket_api = BucketAPI(api_client=api_client)
        result = bucket_api.upload_file(bucket_name, object_name, temp_file_path)

        assert result is None

        os.remove(temp_file_path)
