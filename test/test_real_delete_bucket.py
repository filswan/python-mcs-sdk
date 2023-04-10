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


        self.obj.create_bucket(self.bucket_name)

        result = self.obj.delete_bucket(self.bucket_name)
        assert result is True

    def test_delete_non_existing_bucket_failure(self, shared_current_time):
        logging.info("test_delete_non_existing_bucket_failure")

        bucket_name = "non_existing_bucket" + shared_current_time
        result = self.obj.delete_bucket(bucket_name)
        assert result is False

    def test_delete_empty_bucket_name_failure(self):
        logging.info("test_delete_empty_bucket_name_failure")

        bucket_name = ""
        result = self.obj.delete_bucket(bucket_name)
        assert result is False
