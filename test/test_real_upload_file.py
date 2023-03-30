import pytest
import os


class TestRealUploadFile:
    @pytest.fixture(autouse=True)
    def setup(self, shared_real_bucket):
        self.obj = shared_real_bucket
        yield

    def test_upload_file_success(self, shared_current_time):
        # 先创建一个桶和文件夹
        bucket_name = "test_bucket" + shared_current_time
        self.obj.create_bucket(bucket_name)
        folder_name = "test_folder" + shared_current_time
        self.obj.create_folder(bucket_name, folder_name)
        # 然后上传一个文件
        file_path = "test_file.txt"
        with open(file_path, "w") as f:
            f.write("Test file content" + shared_current_time)
        object_name = folder_name + "/test_file.txt"
        result = self.obj.upload_file(bucket_name, object_name, file_path)
        assert result is not None

        # 删除文件
        os.remove(file_path)

    def test_upload_existing_file_failure(self, shared_current_time):
        # 先创建一个桶和文件夹，然后上传一个文件
        bucket_name = "test_bucket" + shared_current_time
        self.obj.create_bucket(bucket_name)
        folder_name = "test_folder" + shared_current_time
        self.obj.create_folder(bucket_name, folder_name)
        file_path = "test_file.txt"
        with open(file_path, "w") as f:
            f.write("Test file content" + shared_current_time)
        object_name = bucket_name+"/test_file.txt"
        self.obj.upload_file(bucket_name, object_name, file_path)
        # 再次使用相同的对象名称上传文件，预期应该返回None
        result = self.obj.upload_file(bucket_name, object_name, file_path)
        assert result is None

        # 删除文件
        os.remove(file_path)

    def test_upload_existing_file_success(self, shared_current_time):
        # 尝试上传一个已经存在的文件，预期应该返回文件信息
        bucket_name = "test_bucket" + shared_current_time
        self.obj.create_bucket(bucket_name)
        folder_name = "test_folder" + shared_current_time
        self.obj.create_folder(bucket_name, folder_name)
        file_path = "test_file.txt"
        with open(file_path, "w") as f:
            f.write("Test file content" + shared_current_time)
        object_name = bucket_name+"/test_file.txt"
        self.obj.upload_file(bucket_name, object_name, file_path)
        # 再次使用相同的对象名称上传文件，预期应该返回None
        result = self.obj.upload_file(bucket_name, object_name, file_path, replace=True)
        assert result is not None

        # 删除文件
        os.remove(file_path)

    def test_create_object_name(self, shared_current_time):
        # 上传一个不存在的object，预期应该返回对应的object_name
        bucket_name = "test_bucket" + shared_current_time
        self.obj.create_bucket(bucket_name)
        folder_name = "test_folder" + shared_current_time
        self.obj.create_folder(bucket_name, folder_name)
        file_path = "test_file.txt"
        with open(file_path, "w") as f:
            f.write("Test file content" + shared_current_time)
        object_name = bucket_name + "/test_file.txt" + shared_current_time + "1"
        result = self.obj.upload_file(bucket_name, object_name, file_path)
        assert result.object_name == object_name

        # 删除文件
        os.remove(file_path)



