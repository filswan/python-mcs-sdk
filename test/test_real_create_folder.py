import pytest
import datetime

current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


class TestRealCreateFolder:
    @pytest.fixture(autouse=True)
    def setup(self, shared_real_bucket):
        self.obj = shared_real_bucket  # 替换为您的类的实例
        yield

    def test_create_folder_success(self):
        # 先创建一个桶
        bucket_name = "test_bucket" + current_time
        self.obj.create_bucket(bucket_name)
        # 然后在该桶中创建一个文件夹
        folder_name = "test_folder"
        result = self.obj.create_folder(bucket_name, folder_name)
        assert result is True

    def test_create_existing_folder_failure(self):
        # 先创建一个桶和文件夹
        bucket_name = "test_bucket" + current_time
        self.obj.create_bucket(bucket_name)
        folder_name = "test_folder"
        self.obj.create_folder(bucket_name, folder_name)
        # 再次尝试使用相同的文件夹名称创建文件夹，预期应该返回False
        result = self.obj.create_folder(bucket_name, folder_name)
        print(result)
        assert result is False

    def test_create_invalid_folder_name_failure(self):
        # 尝试使用无效的文件夹名称创建文件夹，预期应该返回False
        bucket_name = "test_bucket" + current_time
        self.obj.create_bucket(bucket_name)
        folder_name = ""
        result = self.obj.create_folder(bucket_name, folder_name)
        assert result is False
