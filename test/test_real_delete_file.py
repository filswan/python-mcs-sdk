import os
from pathlib import Path

import pytest


class TestDeleteFile:
    @pytest.fixture(autouse=True)
    def setup(self, shared_real_bucket, shared_current_time):
        self.obj = shared_real_bucket
        self.bucket_name = "test_bucket" + shared_current_time
        self.object_name = "test_file.txt" + shared_current_time
        self.file_path = Path("test_dir")/("test_file.txt" + shared_current_time)
        self.obj.create_bucket(self.bucket_name)
        with open(self.file_path, "w") as f:
            f.write("Test file content" + shared_current_time)
        self.obj.upload_file(self.bucket_name, self.object_name, self.file_path)
        yield

    def test_delete_file_success(self):

        result = self.obj.delete_file(self.bucket_name, self.object_name)
        os.remove(self.file_path)
        assert result is True

    def test_delete_non_existing_file_failure(self):

        result = self.obj.delete_file(self.bucket_name, "non_existing_file.txt")
        os.remove(self.file_path)
        assert result is False

    def test_delete_file_with_invalid_bucket_failure(self, shared_current_time):

        result = self.obj.delete_file("non_existing_bucket" + shared_current_time, self.object_name)
        os.remove(self.file_path)
        assert result is False
