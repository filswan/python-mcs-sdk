import logging
from pathlib import Path

import pytest
import requests_mock
from swan_mcs.common import constants as c
import os

# Set the value of the api to be mocked as False
api_failure_cases = [
    ('BUCKET_LIST', c.BUCKET_LIST, 'get'),
    ('CHECK_UPLOAD', c.CHECK_UPLOAD, 'post'),
    ('UPLOAD_CHUNK', c.UPLOAD_CHUNK, 'post'),
    ('MERGE_FILE', c.MERGE_FILE, 'post'),
    ('CREATE_BUCKET', c.CREATE_BUCKET, 'post'),
    ('FILE_INFO', c.FILE_INFO, 'get'),
]


class TestMockUploadFile:
    # for Upload Replace function and Create object name function, We test it in teat_real_upload_file.py
    # Init mock_requests, Organize all the APIs that need to be mocked
    @pytest.fixture
    def mock_requests(self, shared_bucket_list, shared_current_time, shared_mock_bucket):
        self.object_name = "test-object" + shared_current_time
        self.bucket_name = "test-bucket-1"
        self.temp_file_path = Path("test_dir")/("test_file.txt" + shared_current_time)
        self.temp_file_path.write_text("Test content")
        with requests_mock.Mocker() as m:
            # Mock API requests
            m.get(c.BUCKET_LIST, json={'data': shared_bucket_list})
            m.post(c.UPLOAD_CHUNK, json={"status": "success", "data": ["test-file-name-1"]})
            m.post(c.MERGE_FILE, json={"status": "success",
                                       "data": {"file_id": 12345, "file_hash": "simple_file_hash",
                                                "file_is_exist": False, "ipfs_is_exist": False,
                                                "size": 246493,
                                                "payload_cid": "simple_payload_cid"}})
            m.post(c.CREATE_BUCKET, json={'status': 'success', 'data': 'Bucket created successfully'})
            m.get(c.FILE_INFO, json={"status": "success", "data": {
                'name': "test-file-name-1",
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
        result = shared_mock_bucket.upload_file(self.bucket_name, self.object_name, self.temp_file_path)

        assert result.name == 'test-file-name-1'
        assert result.object_name == self.object_name

    def test_upload_file_already_exists(self, mock_requests, shared_mock_bucket):
        logging.info("test_upload_file_already_exists")

        # Mock custom API requests
        mock_requests.post(c.CHECK_UPLOAD,
                           json={'status': 'success', 'data': {'file_is_exist': True, 'ipfs_is_exist': True}})
        result = shared_mock_bucket.upload_file(self.bucket_name, self.object_name, self.temp_file_path)

        assert result is None

        os.remove(self.temp_file_path)

    @pytest.mark.skip(reason="This test is not working")
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
            shared_mock_bucket.upload_file(self.bucket_name, object_name, self.temp_file_path)

        os.remove(self.temp_file_path)
