import pytest
import requests_mock

from swan_mcs.object import bucket_storage
from swan_mcs.common import constants as c


class TestGetFile:

    @pytest.fixture
    def mock_requests(self, shared_bucket_list, shared_mock_bucket, shared_current_time):
        self.bucket_name = "test-bucket-1"
        self.object_name = "test-object-1"
        self.bucket_id = "simple_bucket_uid"
        self.bucket_api = shared_mock_bucket
        with requests_mock.Mocker() as m:
            m.get(c.GET_FILE, json={"status": "success", "data": {
                'name': "test-file-name-1",
                'address': "simple_address",
                'bucket_uid': "simple_bucket_uid",
                'created_at': "2023-03-28T20:09:45Z",
                'deleted_at': None,
                'file_hash': "simple_file_hash",
                'id': 12345,
                'is_deleted': False,
                'is_folder': False,
                'object_name': 'test-object' + shared_current_time,
                'payload_cid': "simple_payload_cid",
                'pin_status': "Pinned",
                'prefix': "",
                'size': 244029,
                'type': 2,
                'updated_at': "2023-03-28T20:09:45Z"
            }})
            m.get(c.BUCKET_LIST, json={'data': shared_bucket_list})
            yield m

    def test_get_file_success(self, mock_requests):
        file_data = {'id': '12345', 'name': 'test-file-name-1', 'size': 244029}

        result = self.bucket_api.get_file(self.bucket_name, self.object_name)

        assert isinstance(result, bucket_storage.File)
        assert result.name == file_data['name']
        assert result.size == file_data['size']

    def test_get_file_error(self, mock_requests):
        # Mock API requests
        mock_requests.get(c.GET_FILE, json={'status': 'error', 'message': 'An error occurred'})
        result = self.bucket_api.get_file(self.bucket_name, self.object_name)

        assert result is None
