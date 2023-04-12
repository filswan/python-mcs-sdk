import logging

import requests_mock
import pytest
from swan_mcs.common import constants as c


class TestMockGetBucket:
    @pytest.fixture
    def mock_requests(self, shared_bucket_list, shared_mock_bucket):
        self.bucket_api = shared_mock_bucket
        with requests_mock.Mocker() as m:
            m.get(c.BUCKET_LIST, json={'data': shared_bucket_list})

            yield m

    # Test case: get bucket by name
    def test_get_bucket_by_name(self, mock_requests, shared_bucket_list):
        logging.info("test_get_bucket_by_name")
        bucket = self.bucket_api.get_bucket(bucket_name="test-bucket-1")
        assert bucket is not None
        assert bucket.bucket_name == "test-bucket-1"
        assert bucket.bucket_uid == "bucket_uid"

    # Test case: get bucket by id
    def test_get_bucket_by_id(self, mock_requests, shared_bucket_list):
        logging.info("test_get_bucket_by_id")
        bucket = self.bucket_api.get_bucket(bucket_id="bucket_uid")

        assert bucket is not None
        assert bucket.bucket_name == 'test-bucket-1'
        assert bucket.bucket_uid == 'bucket_uid'

    # Test case: get bucket by name and id
    def test_get_bucket_by_name_and_id(self, mock_requests, shared_bucket_list):
        logging.info("test_get_bucket_by_name_and_id")
        bucket = self.bucket_api.get_bucket(bucket_id="bucket_uid", bucket_name="test-bucket-1")

        assert bucket is not None
        assert bucket.bucket_name == 'test-bucket-1'
        assert bucket.bucket_uid == 'bucket_uid'

    # Test case: get bucket by name and id not found
    def test_get_bucket_from_name_not_found(self, mock_requests, shared_bucket_list):
        logging.info("test_get_bucket_from_name_not_found")
        buckets_data = []
        mock_requests.get(c.BUCKET_LIST, json={'data': buckets_data})
        bucket = self.bucket_api.get_bucket(bucket_name="nonexistent-bucket")

        assert bucket is None

    # Test case: get bucket by id not found
    def test_get_bucket_from_id_not_found(self, mock_requests, shared_bucket_list):
        logging.info("test_get_bucket_from_id_not_found")
        buckets_data = []

        mock_requests.get(c.BUCKET_LIST, json={'data': buckets_data})
        bucket = self.bucket_api.get_bucket(bucket_id="nonexistent-bucket_id")

        assert bucket is None
