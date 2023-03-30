import logging

import pytest
import requests_mock
from mcs.common import constants as c
import datetime

current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


class TestMockDeleteBucket:
    @pytest.fixture
    def mock_requests(self, shared_bucket_list):
        with requests_mock.Mocker() as m:
            m.get(c.BUCKET_LIST, json={
                'data': shared_bucket_list
            })
            yield m

    # Test case 1: Delete bucket successfully
    def test_delete_bucket_success(self, mock_requests, shared_mock_bucket):
        logging.info("test_delete_bucket_success")
        bucket_name = "test-bucket" + current_time
        mock_requests.get(c.DELETE_BUCKET, json={'status': 'success'})
        bucket_api = shared_mock_bucket
        result = bucket_api.delete_bucket(bucket_name)

        assert result is True

    # Test case 2: Delete bucket not found
    def test_delete_bucket_not_found(self, mock_requests, shared_mock_bucket, shared_bucket_list):
        logging.info("test_delete_bucket_not_found")
        bucket_name = "test-bucket"
        mock_requests.get(c.DELETE_BUCKET, json={'status': 'failed', 'message': 'Bucket not found'})
        bucket_api = shared_mock_bucket
        result = bucket_api.delete_bucket(bucket_name)
        assert result is False

    # Test case 3: Delete bucket failure
    def test_delete_bucket_failure(self, mock_requests, shared_mock_bucket, shared_bucket_list):
        logging.info("test_delete_bucket_failure")
        bucket_name = "test-bucket"
        mock_requests.get(c.DELETE_BUCKET, json={'status': 'failed'})
        bucket_api = shared_mock_bucket
        result = bucket_api.delete_bucket(bucket_name)

        assert result is False
