import os

import pytest
import requests_mock
from unittest.mock import patch
from mcs.common import constants as c
from test.myUtils.create_temp import create_temp_folder, create_temp_file


class TestMockUploadFolder:
    @pytest.fixture(autouse=True)
    def mock_requests(self, shared_bucket_list, shared_mock_bucket, shared_current_time):
        self.bucket_name = "test-bucket-1"
        self.object_name = "test-object"
        self.folder_path = "/tmp/test-folder"
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
                'name': "IMG_1708.JPG",
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
            yield m

    def test_upload_folder_success(self, mock_requests, shared_bucket_list):
        files = [create_temp_file(1024), create_temp_file(1024), create_temp_file(1024)]
        file_path = [file.name for file in files]
        folder_path = create_temp_folder(file_path)

        result = self.bucket_api.upload_folder(self.bucket_name, self.object_name, folder_path[0].name)
        # 关闭临时文件
        for file in files:
            file.close()

        folder_path[0].cleanup()

        assert len(result) == 3

    def test_upload_folder_empty_folder(self, mock_requests):
        files = []

        # Mock os.listdir and os.path.join
        with patch('os.listdir') as mock_listdir:
            with patch('os.path.join') as mock_path_join:
                mock_listdir.return_value = files
                mock_path_join.side_effect = lambda a, b: f"{a}/{b}"
                result = self.bucket_api.upload_folder(self.bucket_name, self.object_name, create_temp_folder())

        assert result == []
