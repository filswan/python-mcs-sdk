from mcs import ApiClient
from mcs.common.constants import *


class McsAPI(ApiClient):

    def get_params(self):
        return self._request_without_params(GET, MCS_PARAMS)

    def get_price_rate(self):
        return self._request_without_params(GET, PRICE_RATE)

    def get_payment_info(self, payload_cid, wallet_address, source_file_upload_id):
        params = {}
        if payload_cid:
            params['payload_cid'] = payload_cid
        if wallet_address:
            params['wallet_address'] = wallet_address
        if wallet_address:
            params['source_file_upload_id'] = source_file_upload_id
        return self._request_with_params(GET, PAYMENT_INFO, params)

    def get_user_tasks_deals(self, wallet_address):
        params = {}
        if wallet_address:
            params['wallet_address'] = wallet_address
        return self._request_with_params(GET, TASKS_DEALS, params)

    def get_mint_info(self, source_file_upload_id, payload_cid, tx_hash, token_id, mint_address):
        params = {}
        if source_file_upload_id:
            params['source_file_upload_id'] = source_file_upload_id
        if payload_cid:
            params['payload_cid'] = payload_cid
        if tx_hash:
            params['tx_hash'] = tx_hash
        if token_id:
            params['token_id'] = token_id
        if mint_address:
            params['mint_address'] = mint_address
        return self._request_with_params(POST, MINT_INFO, params)

    def upload_file(self, wallet_address, file_path):
        params = {}
        if wallet_address:
            params['wallet_address'] = wallet_address
            params['duration'] = '525'
            params['storage_copy'] = '5'
        return self._request_with_params(GET, UPLOAD_FILE, params, file_path)

    def get_deal_detail(self, wallet_address, source_file_upload_id):
        params = {}
        if wallet_address:
            params['wallet_address'] = wallet_address
        if source_file_upload_id:
            params['source_file_upload_id'] = source_file_upload_id
        return self._request_with_params(GET, DEAL_DETAIL, params)
