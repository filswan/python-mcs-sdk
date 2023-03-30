import logging

import pytest
import requests
import requests_mock
from mcs.common import constants as c

bucket_name = "test-bucket-1"
folder_name = "test-folder"


# 替换这个值为你的测试用API URL
class TestMockCreateFolder:
    @pytest.fixture
    def mock_requests(self, shared_bucket_list):
        with requests_mock.Mocker() as m:
            m.get(c.BUCKET_LIST, json={'data': shared_bucket_list})
            yield m

    # Test case: create folder success
    def test_create_folder_success(self, mock_requests, shared_mock_bucket):
        logging.info("test_create_folder_success")
        mock_requests.post(c.CREATE_FOLDER, json={'status': 'success'})
        bucket_api = shared_mock_bucket
        result = bucket_api.create_folder(bucket_name, folder_name)

        assert result is True

    # Test case: create folder failure
    def test_create_folder_failure(self, mock_requests, shared_bucket_list, shared_mock_bucket):
        logging.info("test_create_folder_failure")
        mock_requests.post(c.CREATE_FOLDER, json={'status': 'failed', 'message': 'Failed to create folder'})

        bucket_api = shared_mock_bucket
        result = bucket_api.create_folder(bucket_name, folder_name)

        assert result is False

    # Test case: create folder failure
    def test_create_folder_exception(self, mock_requests, shared_bucket_list, shared_mock_bucket):
        logging.info("test_create_folder_exception")

        mock_requests.post(c.CREATE_FOLDER, json={}, status_code=404)

        bucket_api = shared_mock_bucket
        result = bucket_api.create_folder(bucket_name, folder_name)

        assert result is False

    # Test case: create folder failure
    def test_create_folder_already_exists(self, mock_requests, shared_mock_bucket):
        logging.info("test_create_folder_already_exists")
        mock_requests.post(c.CREATE_FOLDER,
                           exc=requests.exceptions.RequestException("This bucket already exists"))

        bucket_api = shared_mock_bucket
        result = bucket_api.create_bucket("test-folder")

        assert result is False

    # Test case: create folder failure
    def test_create_invalid_folder_name_failure(self, mock_requests, shared_bucket_list, shared_mock_bucket):
        logging.info("test_create_invalid_folder_name_failure")
        mock_requests.post(c.CREATE_FOLDER, json={'status': 'failed', 'message': 'Folder Name is invalid'})
        bucket_api = shared_mock_bucket
        result = bucket_api.create_bucket("")
        assert result is False
