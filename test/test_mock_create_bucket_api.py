import pytest
import requests
import requests_mock
from mcs.common import constants as c


@pytest.fixture
def mock_requests():
    with requests_mock.Mocker() as m:
        yield m


def test_create_bucket_success(mock_requests, shared_mock_bucket):
    bucket_api = shared_mock_bucket
    mock_requests.post(c.CREATE_BUCKET, json={'status': 'success', 'data': 'Bucket created successfully'})
    result = bucket_api.create_bucket("test-bucket")

    assert result is True


def test_create_bucket_already_exists(mock_requests, shared_mock_bucket):
    mock_requests.post(c.CREATE_BUCKET,
                       exc=requests.exceptions.RequestException("This bucket already exists"))

    bucket_api = shared_mock_bucket
    result = bucket_api.create_bucket("test-bucket")

    assert result is False


def test_create_bucket_failure(mock_requests, shared_mock_bucket):
    mock_requests.post(c.CREATE_BUCKET, json={'status': 'failed', 'message': 'Failed to create bucket'})
    bucket_api = shared_mock_bucket
    result = bucket_api.create_bucket("test-bucket")

    assert result is False
