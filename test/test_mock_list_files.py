import pytest
import requests_mock
from swan_mcs.object import bucket_storage
from swan_mcs.common import constants as c


class TestListFiles:
    @pytest.fixture
    def mock_requests(self, shared_file_list, shared_mock_bucket, shared_bucket_list):
        self.bucket_api = shared_mock_bucket
        self.bucket_name = "test-bucket-1"
        with requests_mock.Mocker() as m:
            m.get(c.BUCKET_LIST, json={'data': shared_bucket_list})
            m.get(c.FILE_LIST, json={"status": "success",
                                     "data": {
                                         "file_list": shared_file_list,
                                         "count": 2
                                     }})
            yield m

    def test_list_files_success(self, mock_requests, shared_file_list):
        result = self.bucket_api.list_files(self.bucket_name)

        assert len(result) == len(shared_file_list)
        assert isinstance(result[0], bucket_storage.File)

    def test_list_files_failure(self, mock_requests):
        mock_requests.get(c.FILE_LIST, json={'status': 'failed', 'message': 'Error listing files'})
        result = self.bucket_api.list_files(self.bucket_name)

        assert result is None
