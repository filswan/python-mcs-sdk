import pytest
import os
from dotenv import load_dotenv
from swan_mcs import OnchainAPI, APIClient


@pytest.mark.skip(reason="no way of currently testing this")
class TestOnchainAPI:
    def login(self):
        load_dotenv(".env_test")
        api_key = os.getenv('api_key')
        access_token = os.getenv('access_token')
        chain_name = os.getenv("chain_name")

        private_key = os.getenv("private_key")
        rpc_endpoint = os.getenv("rpc_endpoint")

        api = OnchainAPI(APIClient(api_key, access_token, chain_name), private_key, rpc_endpoint)
        # print(api.token)

        assert api
        return api

    def test_upload_file(self):
        api = self.login()
        filepath = "/images/log_mcs.png"
        parentpath = os.path.abspath(os.path.dirname(__file__))
        file = api.upload(parentpath + filepath)

        pytest.file = file
        assert file

    def test_pay_file(self):
        api = self.login()
        payment = api.pay(pytest.file.source_file_upload_id, pytest.file.file_size)
        print(payment)

    def test_create_collection(self):
        api = self.login()

        num_collections = len(api.get_collections())
        collection = api.create_collection({"name": 'test-collection-' + str(num_collections)})

        assert len(api.get_collections()) == num_collections + 1

    # def test_mint():
    #     api = login()

    #     mint = api.mint(pytest.file.source_file_upload_id, {"name": 'test-nft', 'image': pytest.file.ipfs_url}, pytest.collection_address)

    #     assert mint["id"] == 1

    def test_get_uploads(self):
        api = self.login()
        deals = api.get_user_tasks_deals()

        file_ids = [deal.source_file_upload_id for deal in deals]

        assert pytest.file.source_file_upload_id in file_ids

    def test_get_deal_detail(self):
        api = self.login()
        detail = api.get_deal_detail(pytest.file.source_file_upload_id)

        assert detail
