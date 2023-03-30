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
        # 然后上传一个文件
        self.file_path = "test_file.txt"
        with open(self.file_path, "w") as f:
            f.write("Test file content" + shared_current_time)
        self.object_name = self.folder_name + "/test_file.txt"
        yield

    def test_upload_file_success(self, shared_current_time):
        result = self.obj.upload_file(self.bucket_name, self.object_name, self.file_path)
        assert result is not None
        # 删除文件
        os.remove(self.file_path)

    def test_upload_existing_file_failure(self, shared_current_time):
        self.obj.upload_file(self.bucket_name, self.object_name, self.file_path)
        result = self.obj.upload_file(self.bucket_name, self.object_name, self.file_path)
        assert result is None

        # 删除文件
        os.remove(self.file_path)

    def test_upload_existing_file_success(self, shared_current_time):
        self.obj.upload_file(self.bucket_name, self.object_name, self.file_path)
        # 再次使用相同的对象名称上传文件，预期应该返回File Info
        result = self.obj.upload_file(self.bucket_name, self.object_name, self.file_path, replace=True)
        assert result is not None

        # 删除文件
        os.remove(self.file_path)

    def test_create_object_name(self, shared_current_time):
        # 上传一个不存在的object，预期应该返回对应的object_name
        object_name = self.bucket_name + "/test_file.txt" + shared_current_time + "1"
        result = self.obj.upload_file(self.bucket_name, object_name, self.file_path)
        assert result.object_name == object_name

        # 删除文件
        os.remove(self.file_path)



