import pytest
from mcs import APIClient


class TestApiKeyLogin:
    @pytest.fixture(autouse=True)
    def setup(self, shared_login_info):
        self.obj = APIClient(shared_login_info['api_key'], shared_login_info['access_token'], shared_login_info['chain_name'])
        yield

    def test_valid_api_key_login(self, shared_login_info):
        self.obj.api_key = shared_login_info['api_key']
        self.obj.access_token = shared_login_info['access_token']
        self.obj.chain_name = shared_login_info['chain_name']
        token = self.obj.api_key_login()
        assert token is not None
        assert isinstance(token, str)

    def test_invalid_api_key_login(self, shared_login_info):
        self.obj.api_key = shared_login_info['wrong_api_key']
        self.obj.access_token = shared_login_info['access_token']
        self.obj.chain_name = shared_login_info['chain_name']
        token = self.obj.api_key_login()
        assert token is None

    def test_invalid_access_token_login(self, shared_login_info):
        self.obj.api_key = shared_login_info['api_key']
        self.obj.access_token = shared_login_info['wrong_access_token']
        self.obj.chain_name = shared_login_info['chain_name']
        token = self.obj.api_key_login()
        assert token is None

    def test_invalid_chain_name_login(self, shared_login_info):
        self.obj.api_key = shared_login_info['api_key']
        self.obj.access_token = shared_login_info['access_token']
        self.obj.chain_name = shared_login_info['wrong_chain_name']
        token = self.obj.api_key_login()
        assert token is None
