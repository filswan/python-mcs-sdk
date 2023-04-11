class TestRealGetGateway():
    def test_real_get_gateway(self, shared_real_api_client):
        gateway = shared_real_api_client.get_gateway()
        assert gateway is not None
