import pytest


class TestRealCreateBucketApi:
    @pytest.fixture(autouse=True)
    def setup(self, shared_real_bucket):
        self.obj = shared_real_bucket
        yield

    def test_create_bucket_success(self,shared_current_time):
        bucket_name = "test_bucket" + shared_current_time
        result = self.obj.create_bucket(bucket_name)
        assert result is True

    def test_create_existing_bucket_failure(self,shared_current_time):
        bucket_name = "test_bucket" + shared_current_time
        self.obj.create_bucket(bucket_name)
        result = self.obj.create_bucket(bucket_name)
        assert result is False

    def test_create_invalid_bucket_name_failure(self):
        # 尝试创建一个无效的桶名
        bucket_name = ""
        result = self.obj.create_bucket(bucket_name)
        assert result is False
