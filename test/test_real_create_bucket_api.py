import datetime
current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


class TestCreateBucketApi:

    def test_create_bucket_success(self, shared_real_bucket):
        bucket_name = "test_bucket" + current_time
        result = shared_real_bucket.create_bucket(bucket_name)
        assert result is True

    def test_create_existing_bucket_failure(self,shared_real_bucket):
        bucket_name = "test_bucket" + current_time
        shared_real_bucket.create_bucket(bucket_name)
        result = shared_real_bucket.create_bucket(bucket_name)
        assert result is False

    def test_create_invalid_bucket_name_failure(self,shared_real_bucket):
        # 尝试创建一个无效的桶名
        bucket_name = ""
        result = shared_real_bucket.create_bucket(bucket_name)
        assert result is False
