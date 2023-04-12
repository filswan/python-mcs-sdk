import logging

import pytest
import requests_mock
from swan_mcs.common import constants as c


class TestMockDeleteBucket:
    @pytest.fixture
    def mock_requests(self, shared_bucket_list, shared_mock_bucket, shared_current_time):
        self.bucket_api = shared_mock_bucket
        self.bucket_name = "test-bucket" + shared_current_time
        with requests_mock.Mocker() as m:
            m.get(c.BUCKET_LIST, json={
                'data': shared_bucket_list
            })
            yield m

    # Test case 1: Delete bucket successfully
    def test_delete_bucket_success(self, mock_requests):
        logging.info("test_delete_bucket_success")
        mock_requests.get(c.DELETE_BUCKET, json={'status': 'success'})
        result = self.bucket_api.delete_bucket(self.bucket_name)

        assert result is True

    # Test case 2: Delete bucket not found
    def test_delete_bucket_not_found(self, mock_requests, shared_bucket_list):
        logging.info("test_delete_bucket_not_found")
        mock_requests.get(c.DELETE_BUCKET, json={'status': 'failed', 'message': 'Bucket not found'})
        result = self.bucket_api.delete_bucket(self.bucket_name)
        assert result is False

    # Test case 3: Delete bucket failure
    def test_delete_bucket_failure(self, mock_requests, shared_bucket_list):
        logging.info("test_delete_bucket_failure")
        mock_requests.get(c.DELETE_BUCKET, json={'status': 'failed'})
        result = self.bucket_api.delete_bucket(self.bucket_name)

        assert result is False
