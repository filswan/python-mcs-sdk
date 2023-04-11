import io
import os
from pathlib import Path
from unittest.mock import patch

import pytest
import requests_mock
from swan_mcs.common import constants as c


class TestDownloadFile:

    @pytest.fixture
    def mock_requests(self, shared_mock_bucket, shared_bucket_list, shared_file_list, tmp_path, shared_current_time):
        self.bucket_api = shared_mock_bucket
        self.bucket_name = "test-bucket-1"
        self.object_name = "test-object-1"

        self.local_filename = Path("test_dir")/("downloaded_file.txt")
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
                'object_name': 'test-object-1',
                'payload_cid': "simple_payload_cid",
                'pin_status': "Pinned",
                'prefix': "",
                'size': 244029,
                'type': 2,
                'updated_at': "2023-03-28T20:09:45Z",
            }})
            m.get(c.BUCKET_LIST, json={'data': shared_bucket_list})
            yield m

    def test_download_file_success(self, mock_requests):
        with patch('urllib.request.urlopen') as m:
            m.return_value = io.BytesIO(b'Test content')
            result = self.bucket_api.download_file(self.bucket_name, self.object_name, self.local_filename)
        assert result is True
        with open(self.local_filename, 'rb') as f:
            assert f.read() == b'Test content'
        os.remove(self.local_filename)

    def test_download_file_not_exists(self, mock_requests):
        mock_requests.get(c.GET_FILE, json={"status": "success", "data": {
            'name': "test-file-name-1",
            'address': "simple_address",
            'bucket_uid': "simple_bucket_uid",
            'created_at': "2023-03-28T20:09:45Z",
            'deleted_at': None,
            'file_hash': "simple_file_hash",
            'id': 12345,
            'is_deleted': False,
            'is_folder': False,
            'object_name': 'test-object-1',
            'payload_cid': "simple_payload_cid",
            'pin_status': "Pinned",
            'prefix': "",
            'size': -1321564651,
            'type': 2,
            'updated_at': "2023-03-28T20:09:45Z",
        }})
        with patch('urllib.request.urlopen') as m:
            m.return_value = io.BytesIO(b'Test content')
            result = self.bucket_api.download_file(self.bucket_name, self.object_name, self.local_filename)

        assert result is None

        os.remove(self.local_filename)
