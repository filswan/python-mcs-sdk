import pytest
import requests
import requests_mock
from mcs.common import constants as c


@pytest.fixture
def mock_requests():
    with requests_mock.Mocker() as m:
        yield m


def test_list_buckets_success(mock_requests, shared_mock_bucket, shared_bucket_list):
    mock_requests.get(c.BUCKET_LIST, json={
        'data':
            shared_bucket_list
    })
    bucket_api = shared_mock_bucket
    bucket_info_list = bucket_api.list_buckets()

    assert len(bucket_info_list) == 2


def test_list_buckets_empty(mock_requests, shared_mock_bucket):
    mock_requests.get(c.BUCKET_LIST, json={'data': []})
    bucket_api = shared_mock_bucket
    bucket_info_list = bucket_api.list_buckets()

    assert len(bucket_info_list) == 0


def test_list_buckets_error(mock_requests, shared_mock_bucket):
    mock_requests.get(c.BUCKET_LIST, exc=requests.exceptions.RequestException("API error"))
    bucket_api = shared_mock_bucket
    bucket_info_list = bucket_api.list_buckets()

    assert bucket_info_list is None
