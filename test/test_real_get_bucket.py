import pytest
import datetime

current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


class TestRealGetBucketApi:
    @pytest.fixture(autouse=True)
    def setup(self, shared_real_bucket):
        self.obj = shared_real_bucket
        yield

    def test_get_bucket_by_name_and_id_success(self):
        # 先创建一个桶
        bucket_name = "test_bucket"
        self.obj.create_bucket(bucket_name)
        # 获取该桶的详细信息
        bucket_id = self.obj._get_bucket_id(bucket_name)
        bucket = self.obj.get_bucket(bucket_name, bucket_id)
        assert bucket is not None

    def test_get_bucket_by_name_success(self):
        # 先创建一个桶
        bucket_name = "test_bucket"
        self.obj.create_bucket(bucket_name)
        # 获取该桶的详细信息
        bucket = self.obj.get_bucket(bucket_name)
        assert bucket is not None

    def test_get_bucket_by_id_success(self):
        # 先创建一个桶
        bucket_name = "test_bucket"
        self.obj.create_bucket(bucket_name)
        # 获取该桶的详细信息
        bucket_id = self.obj._get_bucket_id(bucket_name)
        bucket = self.obj.get_bucket(bucket_id=bucket_id)
        assert bucket is not None

    def test_get_non_existing_bucket_failure(self):
        # 尝试获取一个不存在的桶，预期应该返回None
        bucket_name = "non_existing_bucket"
        bucket_id = "non_existing_bucket_id"
        bucket = self.obj.get_bucket(bucket_name, bucket_id)
        assert bucket is None

    def test_get_invalid_bucket_id_failure(self):
        # 尝试获取一个无效的桶ID，预期应该返回None
        bucket_id = ""
        bucket = self.obj.get_bucket(bucket_id=bucket_id)
        assert bucket is None
