import logging

import pytest
import requests
import requests_mock
from mcs.common import constants as c
import os
import tempfile

api_failure_cases = [
    ('BUCKET_LIST', c.BUCKET_LIST, 'get'),
    ('CHECK_UPLOAD', c.CHECK_UPLOAD, 'post'),
    ('UPLOAD_CHUNK', c.UPLOAD_CHUNK, 'post'),
    ('MERGE_FILE', c.MERGE_FILE, 'post'),
    ('CREATE_BUCKET', c.CREATE_BUCKET, 'post'),
    ('FILE_INFO', c.FILE_INFO, 'get'),
]


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
        logging.info("test_upload_file_success")
        bucket_name = "test-bucket-1"
        object_name = "test-object" + shared_current_time
        file_size = 1024
        temp_file_path = create_temp_file(file_size)

        # Mock API requests
        mock_requests.get(c.BUCKET_LIST, json={'data': shared_bucket_list})

        mock_requests.post(c.UPLOAD_CHUNK, json={"status": "success", "data": ["IMG_1708.JPG"]})
        mock_requests.post(c.MERGE_FILE, json={"status": "success",
                                               "data": {"file_id": 12345, "file_hash": "simple_file_hash",
                                                        "file_is_exist": False, "ipfs_is_exist": False, "size": 246493,
                                                        "payload_cid": "simple_payload_cid"}})
        mock_requests.post(c.CREATE_BUCKET, json={'status': 'success', 'data': 'Bucket created successfully'})
        mock_requests.get(c.FILE_INFO, json={"status": "success", "data": {
            'name': "IMG_1708.JPG",
            'address': "simple_address",
            'bucket_uid': "simple_bucket_uid",
            'created_at': "2023-03-28T20:09:45Z",
            'deleted_at': None,
            'file_hash': "simple_file_hash",
            'id': 12345,
            'is_deleted': False,
            'is_folder': False,
            'object_name': "IMG_1708.JPG",
            'payload_cid': "simple_payload_cid",
            'pin_status': "Pinned",
            'prefix': "",
            'size': 244029,
            'type': 2,
            'updated_at': "2023-03-28T20:09:45Z"
        }})
        mock_requests.get('https://ipfs.io/ipfs/simple_payload_cid',
                          json={'status': 'success', 'data': 'IPFS is working'})
        mock_requests.post(c.CHECK_UPLOAD,
                           json={'status': 'success', 'data': {'file_is_exist': False, 'ipfs_is_exist': False}})
        bucket_api = shared_mock_bucket
        result = bucket_api.upload_file(bucket_name, object_name, temp_file_path)

        assert result.name == 'IMG_1708.JPG'

        os.remove(temp_file_path)

    def test_upload_file_already_exists(self, mock_requests, shared_current_time, shared_bucket_list,
                                        shared_mock_bucket,
                                        shared_file_list):
        logging.info("test_upload_file_already_exists")
        bucket_name = "test-bucket-1"
        object_name = "test-object" + shared_current_time
        file_size = 1024
        temp_file_path = create_temp_file(file_size)

        # Mock API requests
        mock_requests.get(c.BUCKET_LIST, json={'data': shared_bucket_list})
        mock_requests.post(c.CHECK_UPLOAD,
                           json={'status': 'success', 'data': {'file_is_exist': True, 'ipfs_is_exist': True}})
        mock_requests.post(c.UPLOAD_CHUNK, json={"status": "success", "data": ["IMG_1708.JPG"]})
        mock_requests.post(c.MERGE_FILE, json={"status": "success",
                                               "data": {"file_id": 12345, "file_hash": "simple_file_hash",
                                                        "file_is_exist": True, "ipfs_is_exist": True, "size": 246493,
                                                        "payload_cid": "simple_payload_cid"}})
        mock_requests.post(c.CREATE_BUCKET, json={'status': 'success', 'data': 'Bucket created successfully'})
        mock_requests.get(c.FILE_INFO, json={"status": "success", "data": {
            'name': "IMG_1708.JPG",
            'address': "simple_address",
            'bucket_uid': "simple_bucket_uid",
            'created_at': "2023-03-28T20:09:45Z",
            'deleted_at': None,
            'file_hash': "simple_file_hash",
            'id': 12345,
            'is_deleted': False,
            'is_folder': False,
            'object_name': "IMG_1708.JPG",
            'payload_cid': "simple_payload_cid",
            'pin_status': "Pinned",
            'prefix': "",
            'size': 244029,
            'type': 2,
            'updated_at': "2023-03-28T20:09:45Z"
        }})
        mock_requests.get('https://ipfs.io/ipfs/simple_payload_cid',
                          json={'status': 'success', 'data': 'IPFS is working'})

        bucket_api = shared_mock_bucket
        result = bucket_api.upload_file(bucket_name, object_name, temp_file_path)

        assert result is None

        os.remove(temp_file_path)

    @pytest.mark.parametrize("api_case, api_url, api_method", api_failure_cases)
    def test_upload_file_api_failure(self,api_case, api_url, api_method, mock_requests, shared_current_time,
                                     shared_bucket_list, shared_mock_bucket, shared_file_list):
        logging.info("test_upload_file_api_failure")
        bucket_name = "test-bucket-1"
        object_name = "test-object" + shared_current_time
        file_size = 1024
        temp_file_path = create_temp_file(file_size)

        # Common mocks for all test cases
        mock_requests.get(c.BUCKET_LIST, json={'data': shared_bucket_list})
        mock_requests.post(c.CHECK_UPLOAD,
                           json={'status': 'success', 'data': {'file_is_exist': False, 'ipfs_is_exist': False}})
        mock_requests.post(c.UPLOAD_CHUNK, json={"status": "success", "data": ["IMG_1708.JPG"]})
        mock_requests.post(c.MERGE_FILE, json={"status": "success",
                                               "data": {"file_id": 12345, "file_hash": "simple_file_hash",
                                                        "file_is_exist": False, "ipfs_is_exist": False, "size": 246493,
                                                        "payload_cid": "simple_payload_cid"}})
        mock_requests.post(c.CREATE_BUCKET, json={'status': 'success', 'data': 'Bucket created successfully'})
        mock_requests.get(c.FILE_INFO, json={"status": "success", "data": {
            'name': "IMG_1708.JPG",
            'address': "simple_address",
            'bucket_uid': "simple_bucket_uid",
            'created_at': "2023-03-28T20:09:45Z",
            'deleted_at': None,
            'file_hash': "simple_file_hash",
            'id': 12345,
            'is_deleted': False,
            'is_folder': False,
            'object_name': "IMG_1708.JPG",
            'payload_cid': "simple_payload_cid",
            'pin_status': "Pinned",
            'prefix': "",
            'size': 244029,
            'type': 2,
            'updated_at': "2023-03-28T20:09:45Z"
        }})

        # Mock API failure
        if api_method == 'get':
            mock_requests.get(api_url, json={}, status_code=500)
        else:
            mock_requests.post(api_url, json={}, status_code=500)

        logging.info("Testing API failure case: {}".format(api_case))

        with pytest.raises(Exception):
            shared_mock_bucket.upload_file(bucket_name, object_name, temp_file_path)

        os.remove(temp_file_path)
