import logging

import pytest
import mock

class MockResponse:
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

class TestRealBucketListAPI:
    @pytest.fixture(autouse=True)
    def setup(self, shared_real_bucket):
        self.obj = shared_real_bucket

        yield

    def test_list_buckets_success(self):
        logging.info("test_list_buckets_success")
        # 列出所有桶，预期应该返回一个列表
        result = self.obj.list_buckets()
        assert isinstance(result, list)

    @mock.patch('swan_mcs.api_client.APIClient._request_without_params')
    def test_list_buckets_empty_failure(self, mock_req, shared_login_info, shared_real_api_client):
        logging.info("test_list_buckets_empty_failure")
        # 假设没有任何桶存在时，预期列出的结果应该是一个空列表
        # shared_real_api_client.token = shared_login_info['access_token']
        # result = self.obj.list_buckets()
        json_data = {
            "data": None
        }
        mock_response = MockResponse(json_data)
        mock_req.return_value = mock_response
        result = self.obj.list_buckets()
        assert result is None

    def test_list_buckets_invalid_token_failure(self, shared_login_info, shared_real_api_client):
        logging.info("test_list_buckets_invalid_token_failure")
        # 使用无效的令牌尝试列出桶，预期应该返回None
        self.obj.token = "wrong_token"
        result = self.obj.list_buckets()
        assert result is None