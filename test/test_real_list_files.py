import os
from pathlib import Path

import pytest


class TestRealListFiles:
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
        self.obj.delete_bucket(self.bucket_name)

    def test_list_files_success(self):

        file_list = self.obj.list_files(self.bucket_name)
        os.remove(self.file_path)
        assert file_list is not None and len(file_list) > 0

    def test_list_files_with_invalid_bucket_failure(self, shared_current_time):

        file_list = self.obj.list_files("non_existing_bucket" + shared_current_time)
        os.remove(self.file_path)
        assert file_list == []

    def test_list_files_with_limit_success(self):

        limit = 1
        file_list = self.obj.list_files(self.bucket_name, limit=limit)
        os.remove(self.file_path)
        assert len(file_list) == limit

    def test_list_files_with_offset_success(self):

        offset = 1
        file_list = self.obj.list_files(self.bucket_name, offset=offset)
        os.remove(self.file_path)
        assert len(file_list) == len(self.obj.list_files(self.bucket_name)) - offset

    def test_list_files_with_invalid_prefix_success(self):

        file_list = self.obj.list_files(self.bucket_name, prefix="non_existing_prefix")
        os.remove(self.file_path)
        assert file_list == []

    def test_list_files_with_invalid_limit_failure(self):

        file_list = self.obj.list_files(self.bucket_name, limit="invalid_limit")
        os.remove(self.file_path)
        assert file_list is None

    def test_list_files_with_invalid_offset_failure(self):

        file_list = self.obj.list_files(self.bucket_name, offset="invalid_offset")
        os.remove(self.file_path)
        assert file_list is None
