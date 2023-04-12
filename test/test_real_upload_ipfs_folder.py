import os
from pathlib import Path

import pytest


class TestUploadIPFSFolder:
    @pytest.fixture(autouse=True)
    def setup(self, shared_real_bucket, shared_current_time):
        self.obj = shared_real_bucket
        self.bucket_name = "test_bucket" + shared_current_time
        self.folder_name = "test_folder" + shared_current_time
        self.folder_path = Path("test_dir") / ("test_folder" + shared_current_time)
        self.folder_path.mkdir()
        # Create some test files in the folder
        self.file1 = self.folder_path / ("file1.txt" + shared_current_time)
        self.file1.write_text("Test content 1")
        self.file2 = self.folder_path / ("file2.txt" + shared_current_time)
        self.file2.write_text("Test content 2")
        self.obj.create_bucket(self.bucket_name)
        yield

    def test_upload_IPFS_folder_success(self):
        print(self.folder_path)
        # 尝试上传一个文件夹，预期返回成功的文件夹对象
        result = self.obj.upload_ipfs_folder(self.bucket_name, self.folder_name, self.folder_path)
        assert result is not None
        assert result.name == self.folder_name
        os.remove(self.file1)
        os.remove(self.file2)
        os.rmdir(self.folder_path)

    def test_upload_existing_IPFS_folder_failure(self):
        # 尝试上传一个已经存在的文件夹，预期返回None
        result = self.obj.upload_ipfs_folder(self.bucket_name, self.folder_name, self.folder_path)
        print(result)
        assert result is not None
        assert result.name == self.folder_name
        result = self.obj.upload_ipfs_folder(self.bucket_name, self.folder_name, self.folder_path)
        assert result is None
        os.remove(self.file1)
        os.remove(self.file2)
        os.rmdir(self.folder_path)

    def test_upload_IPFS_folder_with_non_existing_bucket_failure(self, shared_current_time):
        # 尝试上传到一个不存在的桶中，预期返回None
        result = self.obj.upload_ipfs_folder("non_existing_bucket" + shared_current_time, self.folder_name,
                                             self.folder_path)
        assert result is None
        os.remove(self.file1)
        os.remove(self.file2)
        os.rmdir(self.folder_path)

    def test_upload_empty_IPFS_folder_success(self, shared_current_time):
        empty_folder_path = Path("test_dir")/("test_empty_folder" + shared_current_time)
        os.mkdir(empty_folder_path)
        result = self.obj.upload_ipfs_folder(self.bucket_name, self.folder_name, empty_folder_path)
        assert result is None
        os.rmdir(empty_folder_path)
