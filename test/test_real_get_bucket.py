import logging

import pytest

class TestRealGetBucketApi:
    @pytest.fixture(autouse=True)
    def setup(self, shared_real_bucket, shared_current_time):
        self.obj = shared_real_bucket

        self.bucket_name = "test_bucket" + shared_current_time
        self.obj.create_bucket(self.bucket_name)
        yield

    def test_get_bucket_by_name_and_id_success(self, shared_current_time):
        logging.info("test_get_bucket_by_name_and_id_success")

        bucket_id = self.obj._get_bucket_id(self.bucket_name)
        bucket = self.obj.get_bucket(self.bucket_name, bucket_id)
        assert bucket is not None

    def test_get_bucket_by_name_success(self, shared_current_time):
        logging.info("test_get_bucket_by_name_success")

        bucket = self.obj.get_bucket(bucket_name=self.bucket_name)
        assert bucket is not None

    def test_get_bucket_by_id_success(self, shared_current_time):
        logging.info("test_get_bucket_by_id_success")

        bucket_id = self.obj._get_bucket_id(self.bucket_name)
        bucket = self.obj.get_bucket(bucket_id=bucket_id)
        assert bucket is not None

    def test_get_non_existing_bucket_failure(self, shared_current_time):
        logging.info("test_get_non_existing_bucket_failure")

        bucket_name = "non_existing_bucket" + shared_current_time
        bucket_id = "non_existing_bucket_id"
        bucket = self.obj.get_bucket(bucket_name, bucket_id)
        assert bucket is None

    def test_get_invalid_bucket_id_failure(self):
        logging.info("test_get_invalid_bucket_id_failure")

        bucket_id = ""
        bucket = self.obj.get_bucket(bucket_id=bucket_id)
        assert bucket is None
