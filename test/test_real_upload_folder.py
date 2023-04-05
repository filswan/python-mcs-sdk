import pytest
import os


class TestBucketAPI:
    @pytest.fixture(autouse=True)
    def setup(self, shared_real_bucket):
        self.obj = shared_real_bucket
        yield

    def test_upload_folder_success(self, shared_current_time):
        # 先创建一个桶和文件夹
        bucket_name = "test_bucket" + shared_current_time
        self.obj.create_bucket(bucket_name)
        folder_name = "test_folder" + shared_current_time
        self.obj.create_folder(bucket_name, folder_name)
        # 然后在该文件夹中上传一个文件夹
        folder_path = "test_folder" + shared_current_time
        os.mkdir(folder_path)

        file_path = os.path.join(folder_path, "test_file.txt")
        with open(file_path, "w") as f:
            f.write("Test file content")
        object_name = "test_folder/test_subfolder"

        result = self.obj.upload_folder(bucket_name, object_name, folder_path)
        os.remove(file_path)
        os.rmdir(folder_path)
        assert len(result) == 1

    def test_upload_empty_folder_failure(self):
        # 尝试上传一个空文件夹，预期应该返回空列表
        bucket_name = "test_bucket"
        self.obj.create_bucket(bucket_name)
        folder_name = "test_folder"
        self.obj.create_folder(bucket_name, folder_name)
        folder_path = "empty_folder"
        os.mkdir(folder_path)
        object_name = "test_folder/empty_folder"
        result = self.obj.upload_folder(bucket_name, object_name, folder_path)
        os.rmdir(folder_path)
        assert len(result) == 0