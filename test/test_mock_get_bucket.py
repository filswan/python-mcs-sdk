import requests_mock
import pytest
from mcs.common import constants as c


@pytest.fixture
def mock_requests():
    with requests_mock.Mocker() as m:
        yield m


def test_get_bucket_by_name(mock_requests, shared_mock_bucket, shared_bucket_list):
    mock_requests.get(c.BUCKET_LIST, json={'data': shared_bucket_list})
    bucket_api = shared_mock_bucket
    bucket = bucket_api.get_bucket(bucket_name="test-bucket-1")

    assert bucket is not None
    assert bucket.bucket_name == "test-bucket-1"
    assert bucket.bucket_uid == "bucket_uid"


def test_get_bucket_by_id(mock_requests, shared_mock_bucket, shared_bucket_list):
    mock_requests.get(c.BUCKET_LIST, json={'data': shared_bucket_list})
    bucket_api = shared_mock_bucket
    bucket = bucket_api.get_bucket(bucket_id="bucket_uid")

    assert bucket is not None
    assert bucket.bucket_name == 'test-bucket-1'
    assert bucket.bucket_uid == 'bucket_uid'


def test_get_bucket_by_name_and_id(mock_requests, shared_mock_bucket, shared_bucket_list):
    mock_requests.get(c.BUCKET_LIST, json={'data': shared_bucket_list})
    bucket_api = shared_mock_bucket
    bucket = bucket_api.get_bucket(bucket_id="bucket_uid", bucket_name="test-bucket-1")

    assert bucket is not None
    assert bucket.bucket_name == 'test-bucket-1'
    assert bucket.bucket_uid == 'bucket_uid'


def test_get_bucket_from_name_not_found(mock_requests, shared_mock_bucket, shared_bucket_list):
    buckets_data = []

    mock_requests.get(c.BUCKET_LIST, json={'data': buckets_data})
    bucket_api = shared_mock_bucket
    bucket = bucket_api.get_bucket(bucket_name="nonexistent-bucket")

    assert bucket is None


def test_get_bucket_from_id_not_found(mock_requests, shared_mock_bucket, shared_bucket_list):
    buckets_data = []

    mock_requests.get(c.BUCKET_LIST, json={'data': buckets_data})
    bucket_api = shared_mock_bucket
    bucket = bucket_api.get_bucket(bucket_id="nonexistent-bucket_id")

    assert bucket is None
