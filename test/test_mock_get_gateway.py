import pytest
import requests_mock

from swan_mcs.common import constants as c


class TestMockGetGateway():
    @pytest.fixture
    def setup(self, shared_mock_api_client):
        self.api_client = shared_mock_api_client
        with requests_mock.Mocker() as m:
            m.get(c.GET_GATEWAY, json={'status': 'success', 'data': ['ipfs.io']})
            yield m

    def test_get_gateway_success(self, setup):
        result = self.api_client.get_gateway()
        assert result is not None

    def test_get_gateway_failure(self, setup):
        setup.get(c.GET_GATEWAY, json={'status': 'failed'}, status_code=500)
        result = self.api_client.get_gateway()
        assert result is None
