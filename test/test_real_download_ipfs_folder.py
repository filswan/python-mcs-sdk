import os
import shutil
from pathlib import Path

import pytest


class TestDownloadIPFSFolder:
    @pytest.fixture(autouse=True)
    def setup(self, shared_real_bucket, shared_current_time):
        self.obj = shared_real_bucket
        self.bucket_name = "test_bucket" + shared_current_time
        self.folder_name = "test_folder" + shared_current_time
        self.folder_path = Path("test_dir") / ("test_folder" + shared_current_time)
        self.object_name = "test_folder" + shared_current_time
        self.obj.create_bucket(self.bucket_name)
        os.mkdir(self.folder_path)
        self.file1 = self.folder_path / ("file1.txt" + shared_current_time)
        self.file1.write_text("Test content 1")
        self.file2 = self.folder_path / ("file2.txt" + shared_current_time)
        self.file2.write_text("Test content 2")
        self.obj.upload_ipfs_folder(self.bucket_name, self.folder_name, self.folder_path)
        yield

    def test_download_IPFS_folder_success(self, shared_current_time):
        # 测试下载已存在的文件夹
        result = self.obj.download_ipfs_folder(self.bucket_name, self.object_name,
                                               Path(self.folder_path) / ("test" + shared_current_time))
        assert result is True
        assert os.path.exists(self.folder_path)

    def test_download_existing_IPFS_folder_failure(self):
        # 测试尝试下载已经存在的文件夹
        result = self.obj.download_ipfs_folder(self.bucket_name, self.object_name, self.folder_path)
        assert result is False

    def test_download_non_existing_IPFS_folder_failure(self):
        # 测试尝试下载不存在的文件夹
        shutil.rmtree(self.folder_path)
        result = self.obj.download_ipfs_folder(self.bucket_name, "non_existing_folder", self.folder_path)
        assert result is False
