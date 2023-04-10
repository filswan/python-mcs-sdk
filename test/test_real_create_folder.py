import logging

import pytest



class TestRealCreateFolder:
    @pytest.fixture(autouse=True)
    def setup(self, shared_real_bucket, shared_current_time):
        self.obj = shared_real_bucket
        # 先创建一个桶和文件夹
        self.bucket_name = "test_bucket" + shared_current_time
        self.obj.create_bucket(self.bucket_name)
        self.folder_name = "test_folder" + shared_current_time
        yield

    def test_create_folder_success(self,shared_current_time):
        logging.info("test_create_folder_success")
        result = self.obj.create_folder(self.bucket_name, self.folder_name)
        assert result is True

    def test_create_existing_folder_failure(self,shared_current_time):
        logging.info("test_create_existing_folder_failure")

        self.obj.create_folder(self.bucket_name, self.folder_name)
        result = self.obj.create_folder(self.bucket_name, self.folder_name)
        assert result is False

    def test_create_invalid_folder_name_failure(self,shared_current_time):
        logging.info("test_create_invalid_folder_name_failure")
        folder_name = ""
        result = self.obj.create_folder(self.bucket_name, folder_name)
        assert result is False
