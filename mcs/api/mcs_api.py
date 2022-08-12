from mcs import ApiClient
from mcs.common.constants import *
import json


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
        return self._request_with_params(GET, PAYMENT_INFO, params, None)

    def get_user_tasks_deals(self, wallet_address, file_name=None):
        params = {}
        if wallet_address:
            params['wallet_address'] = wallet_address
        if file_name:
            params['file_name'] = file_name
        return self._request_with_params(GET, TASKS_DEALS, params, None)

    def get_mint_info(self, source_file_upload_id, payload_cid, tx_hash, token_id, mint_address):
        params = {}
        params['source_file_upload_id'] = source_file_upload_id
        params['payload_cid'] = payload_cid
        params['tx_hash'] = tx_hash
        params['token_id'] = str(token_id)
        params['mint_address'] = mint_address
        return self._request_with_params(POST, MINT_INFO, params, None)

    def upload_file(self, wallet_address, file_path):
        params = {}
        if wallet_address:
            params['wallet_address'] = wallet_address
            params['duration'] = '525'
            params['storage_copy'] = '5'

        files = [
            ('file', (
                file_path, open(file_path, 'rb')))
        ]
        return self._request_with_params(POST, UPLOAD_FILE, params, files)

    def stream_upload_file(self, wallet_address, file_path):
        params = {}
        if wallet_address:
            params['wallet_address'] = wallet_address
            params['duration'] = '525'
            params['storage_copy'] = '5'
            params['file'] = (file_path, open(file_path, 'rb'))

        return self._request_stream_upload(UPLOAD_FILE, params)

    def get_deal_detail(self, wallet_address, source_file_upload_id, deal_id='0'):
        params = {}
        if wallet_address:
            params['wallet_address'] = wallet_address
        if source_file_upload_id:
            params['source_file_upload_id'] = source_file_upload_id
        return self._request_with_params(GET, DEAL_DETAIL+deal_id, params, None)

    def upload_nft_metadata(self, address, file_name, image_url, tx_hash, size):
        params = {}
        if address:
            params['duration'] = '525'
            params['file_type'] = '1'
            params['wallet_address'] = address
        file_url = {}
        if image_url:
            file_url['name'] = file_name
            file_url['image'] = image_url
            file_url['tx_hash'] = tx_hash
            file_url['attributes'] = [
                {
                    "trait_type": "Size",
                    "value": size
                }
            ]
            file_url['external_url'] = image_url
        files = {"fileName": "test", "file": json.dumps(file_url)}
        return self._request_with_params(POST, UPLOAD_FILE, params, files)


