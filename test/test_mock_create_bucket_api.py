import logging

import pytest
import requests
import requests_mock
from swan_mcs.common import constants as c


class TestMockCreateBucket:
    @pytest.fixture
    def mock_requests(self,shared_mock_bucket):
        self.bucket_api = shared_mock_bucket
        with requests_mock.Mocker() as m:
            yield m

    # Test case 1: Create bucket successfully
    def test_create_bucket_success(self, mock_requests, shared_mock_bucket):
        logging.info("test_create_bucket_success")
        mock_requests.post(c.CREATE_BUCKET, json={'status': 'success', 'data': 'Bucket created successfully'})
        result = self.bucket_api.create_bucket("test-bucket")

        assert result is True

    # Test case 2: Create bucket failure
    def test_create_bucket_already_exists(self, mock_requests, shared_mock_bucket):
        logging.info("test_create_bucket_already_exists")
        mock_requests.post(c.CREATE_BUCKET,
                           exc=requests.exceptions.RequestException("This bucket already exists"))

        result = self.bucket_api.create_bucket("test-bucket")

        assert result is False

    # Test case 3: Create bucket failure
    def test_create_bucket_failure(self, mock_requests, shared_mock_bucket):
        logging.info("test_create_bucket_failure")
        mock_requests.post(c.CREATE_BUCKET, json={'status': 'failed', 'message': 'Failed to create bucket'})
        result = self.bucket_api.create_bucket("test-bucket")

        assert result is False
