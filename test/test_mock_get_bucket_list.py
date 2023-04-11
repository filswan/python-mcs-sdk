import logging

import pytest
import requests
import requests_mock
from swan_mcs.common import constants as c


class TestCreateBucket:
    @pytest.fixture
    def mock_requests(self, shared_bucket_list, shared_mock_bucket):
        self.bucket_api = shared_mock_bucket
        with requests_mock.Mocker() as m:
            m.get(c.BUCKET_LIST, json={'data': shared_bucket_list})
            yield m

    # Test case: list buckets
    def test_list_buckets_success(self, mock_requests, shared_bucket_list):
        logging.info("test_list_buckets_success")
        bucket_info_list = self.bucket_api.list_buckets()
        assert len(bucket_info_list) == 2

    # Test case: list buckets empty
    def test_list_buckets_empty(self, mock_requests):
        logging.info("test_list_buckets_empty")
        mock_requests.get(c.BUCKET_LIST, json={'data': []})
        bucket_info_list = self.bucket_api.list_buckets()

        assert len(bucket_info_list) == 0

    # Test case: list buckets error
    def test_list_buckets_error(self, mock_requests):
        logging.info("test_list_buckets_error")
        mock_requests.get(c.BUCKET_LIST, exc=requests.exceptions.RequestException("API error"))
        bucket_info_list = self.bucket_api.list_buckets()

        assert bucket_info_list is None
