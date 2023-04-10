import os

import pytest


class TestDownloadFile:
    @pytest.fixture(autouse=True)
    def setup(self, shared_real_bucket, shared_current_time):
        self.obj = shared_real_bucket
        self.bucket_name = "test_bucket" + shared_current_time
        self.object_name = "test_file.txt" + shared_current_time
        self.file_path = "test_file.txt" + shared_current_time
        self.obj.create_bucket(self.bucket_name)
        with open(self.file_path, "wb") as f:
            f.write(b"Test file content" + shared_current_time.encode())
        self.obj.upload_file(self.bucket_name, self.object_name, self.file_path)
        yield

    def test_download_file_success(self, shared_current_time):
        result = self.obj.download_file(self.bucket_name, self.object_name, "downloaded_file.txt")

        assert result is True
        assert os.path.exists("downloaded_file.txt")
        with open(self.file_path, 'rb') as f:
            assert f.read() == b"Test file content" + shared_current_time.encode()
        os.remove(self.file_path)
        os.remove("downloaded_file.txt")

    def test_download_non_existing_file_failure(self):
        # 尝试下载一个不存在的文件，预期返回False
        result = self.obj.download_file(self.bucket_name, "non_existing_file.txt", "downloaded_file.txt")
        os.remove(self.file_path)
        assert result is False

    def test_download_file_with_invalid_bucket_failure(self):
        # 尝试在一个不存在的桶中下载文件，预期返回False
        result = self.obj.download_file("non_existing_bucket", self.object_name, "downloaded_file.txt")
        os.remove(self.file_path)
        assert result is False
