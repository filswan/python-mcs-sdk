import os
from pathlib import Path

import pytest
import requests_mock
from swan_mcs.common import constants as c


class TestMockUploadFolder:
    @pytest.fixture(autouse=True)
    def mock_requests(self, shared_bucket_list, shared_mock_bucket, shared_current_time):
        self.bucket_name = "test-bucket-1"
        self.object_name = "test-object"

        self.folder_path = Path("test_dir") / ("test-folder" + shared_current_time)
        os.mkdir(self.folder_path)
        self.file1 = self.folder_path / ("file1.txt" + shared_current_time)
        self.file1.write_text("Test content 1")
        self.file2 = self.folder_path / ("file2.txt" + shared_current_time)
        self.file2.write_text("Test content 2")
        self.bucket_api = shared_mock_bucket

        with requests_mock.Mocker() as m:
            m.get(c.BUCKET_LIST, json={'data': shared_bucket_list})
            m.post(c.CREATE_FOLDER, json={'status': 'success', 'data': 'simple_folder_name'})
            m.post(c.CHECK_UPLOAD,
                   json={'status': 'success', 'data': {'file_is_exist': False, 'ipfs_is_exist': False}})
            m.post(c.MERGE_FILE, json={"status": "success",
                                       "data": {"file_id": 12345, "file_hash": "simple_file_hash",
                                                "file_is_exist": False, "ipfs_is_exist": False,
                                                "size": 246493,
                                                "payload_cid": "simple_payload_cid"}})
            m.get(c.FILE_INFO, json={"status": "success", "data": {
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
            m.post(c.UPLOAD_CHUNK, json={"status": "success", "data": ["test-file-name-1"]})
            yield m

    def test_upload_folder_success(self, mock_requests, shared_bucket_list, shared_current_time):
        result = self.bucket_api.upload_folder(self.bucket_name, self.object_name, self.folder_path)
        assert len(result) == 2

    def test_upload_folder_empty_folder(self, mock_requests):
        file_path = Path("test_dir") / "empty_folder"
        os.mkdir(file_path)

        result = self.bucket_api.upload_folder(self.bucket_name, self.object_name, file_path)

        assert result == []

    def test_upload_folder_false(self, mock_requests):
        mock_requests.post(c.CREATE_FOLDER, json={'status': 'error', 'data': 'simple_folder_name'})
        result = self.bucket_api.upload_folder(self.bucket_name, self.object_name, self.folder_path)
        assert result is None
