import logging

import pytest


class TestRealDeleteBucket:
    @pytest.fixture(autouse=True)
    def setup(self, shared_real_bucket, shared_current_time):
        self.obj = shared_real_bucket
        self.bucket_name = "test_bucket" + shared_current_time
        yield

    def test_delete_existing_bucket_success(self):
        logging.info("test_delete_existing_bucket_success")
        # 先创建一个桶

        self.obj.create_bucket(self.bucket_name)
        # 然后删除该桶
        result = self.obj.delete_bucket(self.bucket_name)
        assert result is True

    def test_delete_non_existing_bucket_failure(self):
        logging.info("test_delete_non_existing_bucket_failure")
        # 尝试删除一个不存在的桶，预期应该返回False
        bucket_name = "non_existing_bucket"
        result = self.obj.delete_bucket(bucket_name)
        assert result is False

    def test_delete_empty_bucket_name_failure(self):
        logging.info("test_delete_empty_bucket_name_failure")
        # 尝试删除一个空桶名，预期应该返回False
        bucket_name = ""
        result = self.obj.delete_bucket(bucket_name)
        assert result is False
