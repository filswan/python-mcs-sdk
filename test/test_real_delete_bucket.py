import datetime

current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


class TestBucketAPI:

    def test_delete_existing_bucket_success(self, shared_real_bucket):
        # 先创建一个桶
        bucket_name = "test_bucket" + current_time
        shared_real_bucket.create_bucket(bucket_name)
        # 然后删除该桶
        result = shared_real_bucket.delete_bucket(bucket_name)
        assert result is True

    def test_delete_non_existing_bucket_failure(self, shared_real_bucket):
        # 尝试删除一个不存在的桶，预期应该返回False
        bucket_name = "non_existing_bucket"
        result = shared_real_bucket.delete_bucket(bucket_name)
        assert result is False

    def test_delete_empty_bucket_name_failure(self, shared_real_bucket):
        # 尝试删除一个空桶名，预期应该返回False
        bucket_name = ""
        result = shared_real_bucket.delete_bucket(bucket_name)
        assert result is False
