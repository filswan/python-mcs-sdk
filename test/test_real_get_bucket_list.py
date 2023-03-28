class TestBucketListAPI:

    def test_list_buckets_success(self, shared_real_bucket):
        result = shared_real_bucket.list_buckets()
        assert isinstance(result, list)

    def test_list_buckets_empty_failure(self, shared_real_bucket, shared_login_info, shared_real_api_client):
        # 假设没有任何桶存在时，预期列出的结果应该是一个空列表
        shared_real_api_client.token = shared_login_info['access_token']
        result = shared_real_bucket.list_buckets()
        assert result is None

    def test_list_buckets_invalid_token_failure(self, shared_real_bucket, shared_login_info, shared_real_api_client):
        # 使用无效的令牌尝试列出桶，预期应该返回None
        shared_real_api_client.token = shared_login_info['wrong_access_token']
        result = shared_real_bucket.list_buckets()
        assert result is None
