import os

import pytest

from swan_mcs.object import bucket_storage

class TestRealGetFile:
    @pytest.fixture(autouse=True)
    def setup(self, shared_real_bucket):
        self.obj = shared_real_bucket
        yield

    def test_get_file_success(self, shared_current_time):
        bucket_name = "test_bucket" + shared_current_time
        self.obj.create_bucket(bucket_name)
        object_name = "test_file.txt" + shared_current_time
        file_path = "test_file.txt" + shared_current_time
        with open(file_path, "w") as f:
            f.write("Test file content")
        self.obj.upload_file(bucket_name, object_name, file_path)
        result = self.obj.get_file(bucket_name, object_name)
        os.remove(file_path)
        assert isinstance(result, bucket_storage.File)

    def test_get_non_existing_file_failure(self):

        bucket_name = "test_bucket"
        self.obj.create_bucket(bucket_name)
        object_name = "non_existing_file.txt"
        result = self.obj.get_file(bucket_name, object_name)
        assert result is None

    def test_get_file_with_invalid_bucket_failure(self, shared_current_time):

        bucket_name = "non_existing_bucket" + shared_current_time
        object_name = "test_file.txt"
        result = self.obj.get_file(bucket_name, object_name)
        assert result is None
