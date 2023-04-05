import os

import pytest

import mcs.object.bucket_storage


class TestBucketAPI:
    @pytest.fixture(autouse=True)
    def setup(self, shared_real_bucket):
        self.obj = shared_real_bucket
        yield

    def test_get_file_success(self, shared_current_time):
        # 先创建一个桶和一个文件
        bucket_name = "test_bucket" + shared_current_time
        self.obj.create_bucket(bucket_name)
        object_name = "test_file.txt" + shared_current_time
        file_path = "test_file.txt" + shared_current_time
        with open(file_path, "w") as f:
            f.write("Test file content")
        self.obj.upload_file(bucket_name, object_name, file_path)
        # 然后获取该文件并检查返回值是否是File对象
        result = self.obj.get_file(bucket_name, object_name)
        os.remove(file_path)
        assert isinstance(result, mcs.object.bucket_storage.File)

    def test_get_non_existing_file_failure(self):
        # 尝试获取一个不存在的文件，预期应该返回None
        bucket_name = "test_bucket"
        self.obj.create_bucket(bucket_name)
        object_name = "non_existing_file.txt"
        result = self.obj.get_file(bucket_name, object_name)
        assert result is None

    def test_get_file_with_invalid_bucket_failure(self):
        # 尝试在一个不存在的桶中获取文件，预期应该返回None
        bucket_name = "non_existing_bucket"
        object_name = "test_file.txt"
        result = self.obj.get_file(bucket_name, object_name)
        assert result is None
