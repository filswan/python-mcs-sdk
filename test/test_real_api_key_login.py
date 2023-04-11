import pytest
from swan_mcs import APIClient


class TestRealApiKeyLogin:

    def test_valid_api_key_login(self, shared_login_info):
        api_client = APIClient(shared_login_info['api_key'], shared_login_info['access_token'],
                               shared_login_info['chain_name'])
        print(api_client)
        token = api_client.token
        assert token is not None
        assert isinstance(token, str)

    def test_invalid_api_key_login(self, shared_login_info):
        api_client = APIClient(shared_login_info['wrong_api_key'], shared_login_info['access_token'],
                               shared_login_info['chain_name'])
        token = api_client.token
        assert token is None

    def test_invalid_access_token_login(self, shared_login_info):
        api_client = APIClient(shared_login_info['api_key'], shared_login_info['wrong_access_token'],
                               shared_login_info['chain_name'])
        token = api_client.token
        assert token is None

    def test_invalid_chain_name_login(self, shared_login_info):
        with pytest.raises(AttributeError):
            APIClient(shared_login_info['api_key'], shared_login_info['access_token'],
                      shared_login_info['wrong_chain_name'])
