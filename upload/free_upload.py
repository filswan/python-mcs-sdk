from web3 import Web3

from mcs import McsAPI
from mcs import ContractAPI

from mcs.common.utils import get_amount

import logging

class FreeUpload():

    def __init__(self, wallet_address, private_key, rpc_endpoint, file_path):

        self.wallet_address = wallet_address
        self.private_key = private_key
        self.rpc_endpoint = rpc_endpoint
        self.file_path = file_path
        self.upload_response = None

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
    
    def pay(self):
        api = McsAPI()
        w3_api = ContractAPI(self.rpc_endpoint)
        w3 = Web3(Web3.HTTPProvider(self.rpc_endpoint))

        file_size, w_cid = self.upload_response['file_size'], self.upload_response['w_cid']
        params = api.get_params()["data"]
        rate = api.get_price_rate()["data"]

        amount = get_amount(file_size, rate)
        approve_amount = int(w3.toWei(amount, 'ether') * float(params['pay_multiply_factor']))

        # payment
        try:
            w3_api.approve_usdc(self.wallet_address, self.private_key, approve_amount)
            w3_api.upload_file_pay(self.wallet_address, self.private_key, file_size, w_cid, rate, params)
        except Exception as e:
            logging.error(str(e))
            return 'payment failed: ' + str(e)
        
        return 'payment success'