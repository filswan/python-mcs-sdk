import pytest
import requests_mock
from mcs.common import constants as c
import datetime

current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


class TestMockDeleteBucket:
    @pytest.fixture
    def mock_requests(self):
        with requests_mock.Mocker() as m:
            yield m

    def test_delete_bucket_success(self,mock_requests, shared_mock_bucket, shared_bucket_list):
        bucket_name = "test-bucket" + current_time

        mock_requests.get(c.BUCKET_LIST, json={
            'data': shared_bucket_list
        })
        mock_requests.get(c.DELETE_BUCKET, json={'status': 'success'})
        bucket_api = shared_mock_bucket
        result = bucket_api.delete_bucket(bucket_name)

        assert result is True

    def test_delete_bucket_not_found(self,mock_requests, shared_mock_bucket, shared_bucket_list):
        bucket_name = "test-bucket"
        mock_requests.get(c.BUCKET_LIST, json={
            'data': shared_bucket_list
        })
        mock_requests.get(c.DELETE_BUCKET, status_code=404)

        bucket_api = shared_mock_bucket
        result = bucket_api.delete_bucket(bucket_name)

        assert result is False

    def test_delete_bucket_failure(self,mock_requests, shared_mock_bucket, shared_bucket_list):
        bucket_name = "test-bucket"

        mock_requests.get(c.DELETE_BUCKET, json={'status': 'failed'})
        mock_requests.get(c.BUCKET_LIST, json={
            'data': shared_bucket_list
        })

        bucket_api = shared_mock_bucket
        result = bucket_api.delete_bucket(bucket_name)

        assert result is False
