import logging

import pytest
import requests_mock
from swan_mcs import APIClient
from swan_mcs.common import constants as c
from secrets import compare_digest


class TestMockApiKeyLogin:
    @pytest.fixture
    def mock_requests(self):
        with requests_mock.Mocker() as m:
            yield m

    def test_api_key_login_success(self, mock_requests):
        mock_requests.register_uri(c.POST, c.APIKEY_LOGIN, json={"data": {"jwt_token": "sample_token"}})
        api_client = APIClient(api_key="sample_api_key", access_token="sample_access_token",
                               chain_name="polygon.mumbai")
        token = api_client.token
        assert compare_digest(token, "sample_token")


    @pytest.mark.parametrize("api_key, access_token, chain_name", [
        ("", "sample_access_token", "polygon.mumbai"),
        ("sample_api_key", "", "polygon.mumbai")
    ])
    def test_api_key_login_empty_params(self, mock_requests, api_key, access_token, chain_name):
        logging.info("test_api_key_login_empty_params")
        mock_requests.register_uri(c.POST, c.APIKEY_LOGIN, status_code=400)
        api_client = APIClient(api_key=api_key, access_token=access_token, chain_name=chain_name)
        token = api_client.api_key_login()
        assert token is None

    def test_api_key_login_empty_chain_name(self, mock_requests):
        logging.info("test_api_key_login_empty_chain_name")
        mock_requests.register_uri(c.POST, c.APIKEY_LOGIN, status_code=400)
        api_client = APIClient(api_key="sample_api_key", access_token="sample_access_token")
        token = api_client.api_key_login()
        assert token is None

    def test_api_key_login_invalid_credentials(self, mock_requests):
        logging.info("test_api_key_login_invalid_credentials")
        mock_requests.register_uri(c.POST, c.APIKEY_LOGIN, status_code=401)
        api_client = APIClient(api_key="wrong_api_key", access_token="wrong_access_token",
                               chain_name="polygon.mumbai")
        token = api_client.api_key_login()
        assert token is None
