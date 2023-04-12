import logging

import pytest


class TestRealCreateBucketApi:
    @pytest.fixture(autouse=True)
    def setup(self, shared_real_bucket, shared_current_time):
        self.obj = shared_real_bucket
        self.bucket_name = "test_bucket" + shared_current_time
        yield

    def test_create_bucket_success(self):
        logging.info("test_create_bucket_success")
        result = self.obj.create_bucket(self.bucket_name)
        assert result is True

    def test_create_existing_bucket_failure(self):
        logging.info("test_create_existing_bucket_failure")
        self.obj.create_bucket(self.bucket_name)
        result = self.obj.create_bucket(self.bucket_name)
        assert result is False

    def test_create_invalid_bucket_name_failure(self):
        logging.info("test_create_invalid_bucket_name_failure")
        # 尝试创建一个无效的桶名
        bucket_name = ""
        result = self.obj.create_bucket(bucket_name)
        assert result is False
