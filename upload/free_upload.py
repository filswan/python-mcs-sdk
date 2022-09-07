from distutils.command.upload import upload
from mcs import McsAPI
from mcs import ContractAPI
from mcs.common.constants import MCS_API

class FreeUpload():

    def __init__(self, wallet_address, private_key, web3_api, file_path):

        self.wallet_address = wallet_address
        self.private_key = private_key
        self.web3_api = web3_api
        self.file_path = file_path
        self.upload_response = None

    def free_upload(self):
        file_data = self.upload()
        if file_data['status'] == 'Free':
            return 'free upload'
        self.pay()
        return 'paid upload'
        

    def upload(self):
        api = McsAPI()

        upload_file = api.upload_file(self.wallet_address, self.file_path)
        file_data = upload_file["data"]
        self.upload_response = file_data
        return file_data
    
    def pay(self):
        api = MCS_API()
        w3_api = ContractAPI(self.web3_api)

        file_size, w_cid = self.upload_response['file_size'], self.upload_response['w_cid']
        params = api.get_params()["data"]
        rate = api.get_price_rate()["data"]

        # payment
        try:
            w3_api.approve_usdc(self.wallet_address, self.private_key, "1")
            w3_api.upload_file_pay(self.wallet_address, self.private_key, file_size, w_cid, rate, params)
        except Exception as e:
            return 'payment failed: ' + e
        
        return 'payment success'