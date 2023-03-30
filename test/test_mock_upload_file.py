import logging

import pytest
import requests
import requests_mock
from mcs.common import constants as c
import os
import tempfile

# Set the value of the api to be mocked as False
api_failure_cases = [
    ('BUCKET_LIST', c.BUCKET_LIST, 'get'),
    ('CHECK_UPLOAD', c.CHECK_UPLOAD, 'post'),
    ('UPLOAD_CHUNK', c.UPLOAD_CHUNK, 'post'),
    ('MERGE_FILE', c.MERGE_FILE, 'post'),
    ('CREATE_BUCKET', c.CREATE_BUCKET, 'post'),
    ('FILE_INFO', c.FILE_INFO, 'get'),
]
# setup the temporary file
file_size = 1024
bucket_name = "test-bucket-1"


# Create a temporary file
def create_temp_file(size, content=None):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        if content is None:
            content = b'\0' * size
        f.write(content)
        temp_file_path_in_create = f.name
    return temp_file_path_in_create


# setup the temporary file
temp_file_path = create_temp_file(file_size)


class TestMockUploadFile:
    # for Upload Replace function and Create object name function, We test it in teat_real_upload_file.py
    # Init mock_requests, Organize all the APIs that need to be mocked
    @pytest.fixture
    def mock_requests(self, shared_bucket_list, shared_current_time, shared_mock_bucket):
        with requests_mock.Mocker() as m:
            # Mock API requests
            m.get(c.BUCKET_LIST, json={'data': shared_bucket_list})
            m.post(c.UPLOAD_CHUNK, json={"status": "success", "data": ["IMG_1708.JPG"]})
            m.post(c.MERGE_FILE, json={"status": "success",
                                       "data": {"file_id": 12345, "file_hash": "simple_file_hash",
                                                "file_is_exist": False, "ipfs_is_exist": False,
                                                "size": 246493,
                                                "payload_cid": "simple_payload_cid"}})
            m.post(c.CREATE_BUCKET, json={'status': 'success', 'data': 'Bucket created successfully'})
            m.get(c.FILE_INFO, json={"status": "success", "data": {
                'name': "IMG_1708.JPG",
                'address': "simple_address",
                'bucket_uid': "simple_bucket_uid",
                'created_at': "2023-03-28T20:09:45Z",
                'deleted_at': None,
                'file_hash': "simple_file_hash",
                'id': 12345,
                'is_deleted': False,
                'is_folder': False,
                'object_name': 'test-object' + shared_current_time,
                'payload_cid': "simple_payload_cid",
                'pin_status': "Pinned",
                'prefix': "",
                'size': 244029,
                'type': 2,
                'updated_at': "2023-03-28T20:09:45Z"
            }})
            m.post(c.CHECK_UPLOAD,
                   json={'status': 'success', 'data': {'file_is_exist': False, 'ipfs_is_exist': False}})

            yield m

    def test_upload_file_success(self, mock_requests, shared_current_time, shared_bucket_list, shared_mock_bucket):

        logging.info("test_upload_file_success")
        object_name = "test-object" + shared_current_time
        result = shared_mock_bucket.upload_file(bucket_name, object_name, temp_file_path)

        assert result.name == 'IMG_1708.JPG'
        assert result.object_name == object_name

        os.remove(temp_file_path)

    def test_upload_file_already_exists(self, mock_requests, shared_current_time, shared_bucket_list,
                                        shared_mock_bucket):
        logging.info("test_upload_file_already_exists")
        object_name = "test-object" + shared_current_time

        # Mock custom API requests
        mock_requests.post(c.CHECK_UPLOAD,
                           json={'status': 'success', 'data': {'file_is_exist': True, 'ipfs_is_exist': True}})
        result = shared_mock_bucket.upload_file(bucket_name, object_name, temp_file_path)

        assert result is None

        os.remove(temp_file_path)

    @pytest.mark.skip(reason="Need to fix this test case")
    @pytest.mark.parametrize("api_case, api_url, api_method", api_failure_cases)
    def test_upload_file_api_failure(self, api_case, api_url, api_method, mock_requests, shared_current_time,
                                     shared_mock_bucket):
        logging.info("test_upload_file_api_failure")
        object_name = "test-object" + shared_current_time
        # Mock API failure
        if api_method == 'get':
            mock_requests.get(api_url, json={}, status_code=500)
        else:
            mock_requests.post(api_url, json={}, status_code=500)

        logging.info("Testing API failure case: {}".format(api_case))

        with pytest.raises(Exception):
            shared_mock_bucket.upload_file(bucket_name, object_name, temp_file_path)

        os.remove(temp_file_path)
