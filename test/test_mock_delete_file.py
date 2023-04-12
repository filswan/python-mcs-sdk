import pytest
import requests_mock
from swan_mcs.common import constants as c


class TestDeleteFile:
    @pytest.fixture
    def mock_requests(self, shared_mock_bucket, shared_bucket_list, shared_file_list):
        self.bucket_name = "test-bucket-1"
        self.object_name = "test-object-1/test-file-name-1"
        self.file_id = 12345
        self.bucket_api = shared_mock_bucket
        with requests_mock.Mocker() as m:
            m.get(c.DELETE_FILE, json={'status': 'success'})
            m.get(c.BUCKET_LIST, json={'data': shared_bucket_list})
            m.get(c.FILE_LIST, json={"status": "success",
                                     "data": {
                                         "file_list": shared_file_list,
                                         "count": 2
                                     }})
            yield m

    def test_delete_file_success(self, mock_requests):
        result = self.bucket_api.delete_file(self.bucket_name, self.object_name)

        assert result is True

    def test_delete_file_failure(self, mock_requests):
        # Mock API requests
        mock_requests.get(c.DELETE_FILE, json={'status': 'failed'})
        result = self.bucket_api.delete_file(self.bucket_name, self.object_name)

        assert result is False

    def test_delete_file_not_exits(self, mock_requests):
        result = self.bucket_api.delete_file(self.bucket_name, "self.object_name")

        assert result is False

    def test_delete_file_in_not_exits_bucket(self, mock_requests):
        result = self.bucket_api.delete_file("self.bucket_name", self.object_name)

        assert result is False
