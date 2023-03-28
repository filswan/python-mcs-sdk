import pytest
import requests_mock
from mcs import APIClient
from mcs.common import constants as c
from secrets import compare_digest


# 测试成功登录
def test_api_key_login_success():
    with requests_mock.Mocker() as m:
        m.register_uri(c.POST, c.APIKEY_LOGIN, json={"data": {"jwt_token": "sample_token"}})
        api_client = APIClient(api_key="sample_api_key", access_token="sample_access_token",
                               chain_name="polygon.mumbai")
        token = api_client.api_key_login()
        assert compare_digest(token, "sample_token")


# 测试参数为空的情况
@pytest.mark.parametrize("api_key, access_token, chain_name", [
    ("", "sample_access_token", "polygon.mumbai"),
    ("sample_api_key", "", "polygon.mumbai"),
    ("sample_api_key", "sample_access_token", "")
])
def test_api_key_login_empty_params(api_key, access_token, chain_name):
    with requests_mock.Mocker() as m:
        m.register_uri(c.POST, c.APIKEY_LOGIN, status_code=400)
        print(chain_name)
        api_client = APIClient(api_key=api_key, access_token=access_token, chain_name=chain_name)
        token = api_client.api_key_login()
        assert token is None


# 测试chain_name参数为空的情况
@pytest.mark.parametrize("api_key, access_token, chain_name", [
    ("sample_api_key", "sample_access_token", "")
])
def test_api_key_login_empty_params(api_key, access_token, chain_name):
    with requests_mock.Mocker() as m:
        m.register_uri(c.POST, c.APIKEY_LOGIN, status_code=400)
        api_client = APIClient(api_key=api_key, access_token=access_token)
        token = api_client.api_key_login()
        assert token is None


# 测试错误的API密钥或访问令牌
def test_api_key_login_invalid_credentials():
    with requests_mock.Mocker() as m:
        m.register_uri(c.POST, c.APIKEY_LOGIN, status_code=401)
        api_client = APIClient(api_key="wrong_api_key", access_token="wrong_access_token",
                               chain_name="polygon.mumbai")
        token = api_client.api_key_login()
        assert token is None
