from mcs import McsAPI
from mcs import ContractAPI
from mcs.common.params import Params
from mcs.common.utils import get_amount
import logging


class MCSUpload():
    def __init__(self, chain_name, wallet_address, private_key, rpc_endpoint, file_path):
        self.chain_name = chain_name
        self.wallet_address = wallet_address
        self.private_key = private_key
        self.rpc_endpoint = rpc_endpoint
        self.file_path = file_path
        self.upload_response = None
        self.payment_tx_hash = None

        self.api = McsAPI(Params(self.chain_name).MCS_API)
        self.api.get_jwt_token(self.wallet_address, self.private_key, self.chain_name)
        self.w3_api = ContractAPI(self.rpc_endpoint, self.chain_name)

    def approve_token(self, amount):
        return self.w3_api.approve_usdc(self.wallet_address, self.private_key, amount)

    def stream_upload(self):
        upload_file = self.api.stream_upload_file(self.wallet_address, self.file_path)
        file_data = upload_file["data"]
        need_pay = 0
        if file_data["status"] == "Free":
            self.upload_response = file_data

        else:
            self.upload_response = file_data
            need_pay = 1
        return file_data, need_pay

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
            self.payment_tx_hash = self.w3_api.upload_file_pay(self.wallet_address, self.private_key, file_size, w_cid,
                                                               rate,
                                                               params)
        except Exception as e:
            logging.error(str(e))
            return 'payment failed: ' + str(e)

        return self.payment_tx_hash

    def mint(self, file_name):
        file_data = self.upload_response
        source_file_upload_id, nft_uri, file_size = file_data['source_file_upload_id'], file_data['ipfs_url'], \
                                                    file_data['file_size']
        meta_url = \
            self.api.upload_nft_metadata(self.wallet_address, file_name, nft_uri, self.payment_tx_hash, file_size)[
                'data'][
                'ipfs_url']
        tx_hash, token_id = self.w3_api.mint_nft(self.wallet_address, self.private_key, meta_url)
        response = self.api.get_mint_info(source_file_upload_id, None, tx_hash, token_id, self.wallet_address)
        return tx_hash, token_id, response
