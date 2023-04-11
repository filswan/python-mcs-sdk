import os

import pytest
import requests_mock

from swan_mcs.object import bucket_storage
from swan_mcs.common import constants as c

from pathlib import Path


class TestMockUploadIpfsFolder:
    @pytest.fixture
    def mock_requests(self, shared_current_time, shared_bucket_list, shared_mock_bucket, shared_ipfs_file_list):
        self.bucket_name = "test-bucket-1"
        self.object_name = "test-object-1"

        self.folder_path = Path("test_dir")/("test_folder" + shared_current_time)
        self.folder_path.mkdir()
        # Create some test files in the folder
        self.file1 = self.folder_path / ("file1.txt" + shared_current_time)
        self.file1.write_text("Test content 1")
        self.file2 = self.folder_path / ("file2.txt" + shared_current_time)
        self.file2.write_text("Test content 2")

        self.bucket_api = shared_mock_bucket
        with requests_mock.Mocker() as m:
            m.get(c.BUCKET_LIST, json={'data': shared_bucket_list})
            m.post(c.CREATE_FOLDER, json={'status': 'success', 'data': 'simple_folder_name'})
            m.post(c.PIN_IPFS, json={'status': 'success', 'data': shared_ipfs_file_list[0]})
            yield m

    def test_upload_ipfs_folder_success(self, mock_requests, tmp_path, shared_current_time):
        # Run the method
        result = self.bucket_api.upload_ipfs_folder(self.bucket_name, self.object_name, self.folder_path)

        # Check the result
        assert result is not None
        assert isinstance(result, bucket_storage.File)
        assert result.id == 1
        assert result.name == "test_ipfs_file_name-1"
        os.remove(self.folder_path / ("file1.txt" + shared_current_time))
        os.remove(self.folder_path / ("file2.txt" + shared_current_time))
        os.rmdir(self.folder_path)

    def test_upload_ipfs_folder_with_wrong_param(self, mock_requests, tmp_path, shared_current_time):
        # Run the method
        result = self.bucket_api.upload_ipfs_folder("self.bucket_name", self.object_name, self.folder_path)

        # Check the result
        assert result is None
        os.remove(self.folder_path / ("file1.txt" + shared_current_time))
        os.remove(self.folder_path / ("file2.txt" + shared_current_time))
        os.rmdir(self.folder_path)
