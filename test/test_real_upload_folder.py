from pathlib import Path

import pytest
import os


class TestRealUploadFolder:
    @pytest.fixture(autouse=True)
    def setup(self, shared_real_bucket, shared_current_time):
        self.obj = shared_real_bucket
        self.bucket_name = "test_bucket" + shared_current_time
        self.obj.create_bucket(self.bucket_name)
        self.folder_name = "test_folder" + shared_current_time
        self.obj.create_folder(self.bucket_name, self.folder_name)
        self.folder_path = Path("test_dir") / ("test_folder" + shared_current_time)
        os.mkdir(self.folder_path)
        self.file_path = os.path.join(self.folder_path, "test_file.txt" + shared_current_time)
        with open(self.file_path, "w") as f:
            f.write("Test file content")
        self.object_name = "test_folder/test_subfolder"
        yield

    def test_upload_folder_success(self, shared_current_time):
        result = self.obj.upload_folder(self.bucket_name, self.object_name, self.folder_path)
        os.remove(self.file_path)
        os.rmdir(self.folder_path)
        assert len(result) == 1

    def test_upload_empty_folder(self, shared_current_time):
        folder_path = Path("test_dir")/"empty_folder"
        os.mkdir(folder_path)
        object_name = "test_folder/empty_folder"
        result = self.obj.upload_folder(self.bucket_name, object_name, folder_path)
        os.rmdir(folder_path)
        assert len(result) == 0

    def test_upload_folder_in_a_non_exits_folder(self, shared_current_time):
        bucket_name = "test_bucket" + shared_current_time
        folder_path = "empty_folder" + shared_current_time
        os.mkdir(folder_path)
        object_name = "test_folder/empty_folder" + shared_current_time
        result = self.obj.upload_folder(bucket_name, object_name, folder_path)
        os.rmdir(folder_path)
        assert len(result) == 0

