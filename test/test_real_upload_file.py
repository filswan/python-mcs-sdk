from pathlib import Path

import pytest
import os


class TestRealUploadFile:
    @pytest.fixture(autouse=True)
    def setup(self, shared_real_bucket, shared_current_time):
        self.obj = shared_real_bucket
        self.bucket_name = "test_bucket" + shared_current_time
        self.obj.create_bucket(self.bucket_name)
        self.folder_name = "test_folder" + shared_current_time
        self.obj.create_folder(self.bucket_name, self.folder_name)
        self.file_path = Path("test_dir") / "test_file.txt"
        with open(self.file_path, "w") as f:
            f.write("Test file content" + shared_current_time)
        self.object_name = self.folder_name + "/test_file.txt"
        yield

    def test_upload_file_success(self, shared_current_time):
        result = self.obj.upload_file(self.bucket_name, self.object_name, self.file_path)
        assert result is not None

        os.remove(self.file_path)

    def test_upload_existing_file_failure(self, shared_current_time):
        self.obj.upload_file(self.bucket_name, self.object_name, self.file_path)
        result = self.obj.upload_file(self.bucket_name, self.object_name, self.file_path)
        assert result is None

        os.remove(self.file_path)

    def test_upload_existing_file_success(self, shared_current_time):
        self.obj.upload_file(self.bucket_name, self.object_name, self.file_path)

        result = self.obj.upload_file(self.bucket_name, self.object_name, self.file_path, replace=True)
        assert result is not None

        os.remove(self.file_path)

    def test_create_object_name(self, shared_current_time):
        object_name = self.bucket_name + "/test_file.txt" + shared_current_time + "1"
        result = self.obj.upload_file(self.bucket_name, object_name, self.file_path)
        assert result.object_name == object_name

        os.remove(self.file_path)

    def test_upload_file_with_wrong_bucket(self, shared_current_time):
        result = self.obj.upload_file("self.bucket_name", self.object_name, self.file_path)
        assert result is None

        os.remove(self.file_path)