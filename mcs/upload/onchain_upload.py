from mcs import APIClient
from mcs.contract import ContractClient
from mcs.common.utils import get_amount
from mcs.api import OnchainAPI
import logging
from web3 import Web3


class OnchainUpload():
    def __init__(self, chain_name, private_key, rpc_endpoint, api_key, access_token, file_path):
        self.chain_name = chain_name
        self.private_key = private_key
        self.rpc_endpoint = rpc_endpoint
        self.api_key = api_key
        self.access_token = access_token
        self.wallet_address = Web3(Web3.HTTPProvider(self.rpc_endpoint)) \
            .eth.account.privateKeyToAccount(self.private_key).address
        self.file_path = file_path
        self.api = APIClient(self.api_key, self.access_token, self.chain_name)
        self.onchain = OnchainAPI(self.api)
        self.w3_api = ContractClient(self.rpc_endpoint, self.chain_name)

    def approve_token(self, amount):
        return self.w3_api.approve_usdc(self.wallet_address, self.private_key, amount)

    def simple_upload(self, amount):
        self.approve_token(amount)
        self.stream_upload()
        payment_hash = self.pay()
        return payment_hash

    def stream_upload(self):
        upload_file = self.onchain.stream_upload_file(self.wallet_address, self.file_path)
        file_data = upload_file["data"]
        self.upload_response = file_data

    def estimate_amount(self):
        file_size = self.upload_response['file_size']
        rate = self.api.get_price_rate()["data"]
        amount = get_amount(file_size, rate)
        return amount

    def pay(self):
        file_size, w_cid = self.upload_response['file_size'], self.upload_response['w_cid']
        params = self.api.get_params()["data"]
        rate = self.api.get_price_rate()["data"]
        # payment
        try:
            self.payment_tx_hash = self.w3_api.upload_file_pay(self.wallet_address, self.private_key,
                                                               file_size, w_cid, rate, params)
        except Exception as e:
            logging.error(str(e))
            return 'payment failed: ' + str(e)

        return self.payment_tx_hash

    def mint(self, file_name):
        file_data = self.upload_response
        source_file_upload_id, nft_uri, file_size = file_data['source_file_upload_id'], file_data['ipfs_url'], \
            file_data['file_size']
        meta_url = \
            self.onchain.upload_nft_metadata(self.wallet_address, file_name, nft_uri, self.payment_tx_hash, file_size)[
                'data'][
                'ipfs_url']
        tx_hash, token_id = self.w3_api.mint_nft(self.wallet_address, self.private_key, meta_url)
        response = self.onchain.get_mint_info(source_file_upload_id, None,
                                          tx_hash, token_id, self.api.get_params()["data"]['mint_contract_address'])
        return tx_hash, token_id, response
