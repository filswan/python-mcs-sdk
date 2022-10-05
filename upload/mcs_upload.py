from web3 import Web3

from mcs import McsAPI
from mcs import ContractAPI

from mcs.common.utils import get_amount, get_contract_abi
from mcs.common.constants import USDC_ABI, USDC_TOKEN, SWAN_PAYMENT_ADDRESS

import logging

class MCSUpload():

    def __init__(self, wallet_address, private_key, rpc_endpoint, file_path):

        self.wallet_address = wallet_address
        self.private_key = private_key
        self.rpc_endpoint = rpc_endpoint
        self.file_path = file_path
        self.upload_response = None
        self.payment_txhash = None
    
    def change_file(self, file_path):
        self.file_path = file_path
        return self.file_path

    def check_allowance(self):       
        w3 = Web3(Web3.HTTPProvider(self.rpc_endpoint))
        usdc_abi = get_contract_abi(USDC_ABI)
        token = w3.eth.contract(USDC_TOKEN, abi=usdc_abi)
        al = token.functions.allowance(self.wallet_address, SWAN_PAYMENT_ADDRESS).call()

    def approve_token(self, amount):
        w3_api = ContractAPI(self.rpc_endpoint)
        return w3_api.approve_usdc(self.wallet_address, self.private_key, amount)

    def free_upload(self):
        file_data = self.upload()
        if file_data['status'] == 'Free':
            return 'free upload'
        result = self.pay()
        return result
        
    def free_stream_upload(self):
        file_data = self.stream_upload()
        if file_data['status'] == 'Free':
            return 'free stream upload'
        result = self.pay()
        return result

    def upload(self):
        api = McsAPI()

        upload_file = api.upload_file(self.wallet_address, self.file_path)
        file_data = upload_file["data"]
        self.upload_response = file_data
        return file_data

    def stream_upload(self):
        api = McsAPI()

        upload_file = api.stream_upload_file(self.wallet_address, self.file_path)
        file_data = upload_file["data"]
        self.upload_response = file_data
        return file_data

    def estimate_amount(self):
        api = McsAPI()

        file_size = self.upload_response['file_size']
        rate = api.get_price_rate()["data"]

        amount = get_amount(file_size, rate)
        return amount

    def pay(self):
        api = McsAPI()
        w3_api = ContractAPI(self.rpc_endpoint)

        file_size, w_cid = self.upload_response['file_size'], self.upload_response['w_cid']
        params = api.get_params()["data"]
        rate = api.get_price_rate()["data"]

        # payment
        try:
            self.payment_txhash = w3_api.upload_file_pay(self.wallet_address, self.private_key, file_size, w_cid, rate, params)
        except Exception as e:
            logging.error(str(e))
            return 'payment failed: ' + str(e)
        
        return 'payment success'
    
    def mint(self, file_name):
        api = McsAPI()
        w3_api = ContractAPI(self.rpc_endpoint)

        file_data = self.upload_response
        source_file_upload_id, nft_uri, file_size = file_data['source_file_upload_id'], file_data['ipfs_url'], file_data['file_size']
        meta_url = api.upload_nft_metadata(self.wallet_address, file_name, nft_uri, self.payment_txhash, file_size)['data']['ipfs_url']
        tx_hash, token_id = w3_api.mint_nft(self.wallet_address, self.private_key, meta_url)
        response = api.get_mint_info(source_file_upload_id, None, tx_hash, token_id, self.wallet_address)
        return tx_hash, token_id, response