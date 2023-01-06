from mcs import ApiClient
from mcs.common.constants import *
import json


class McsClient(ApiClient):

    def __init__(self, url):
        self.MCS_API = url
        self.token = None

    def get_params(self):
        return self._request_without_params(GET, MCS_PARAMS, self.MCS_API, self.token)

    def get_price_rate(self):
        return self._request_without_params(GET, PRICE_RATE, self.MCS_API, self.token)

    def get_payment_info(self, source_file_upload_id):
        params = {}
        if source_file_upload_id:
            params['source_file_upload_id'] = source_file_upload_id
        return self._request_with_params(GET, PAYMENT_INFO, self.MCS_API, params, self.token, None)

    def get_user_tasks_deals(self, page_number=None, page_size=None, file_name=None, status=None):
        params = {}
        if page_number:
            params['page_number'] = page_number
        if page_size:
            params['page_size'] = page_size
        if file_name:
            params['file_name'] = file_name
        if status:
            params['status'] = status
        return self._request_with_params(GET, TASKS_DEALS, self.MCS_API, params, self.token, None)

    def get_mint_info(self, source_file_upload_id, payload_cid, tx_hash, token_id, mint_address):
        params = {'source_file_upload_id': source_file_upload_id, 'payload_cid': payload_cid, 'tx_hash': tx_hash,
                  'token_id': int(token_id), 'mint_address': mint_address}
        return self._request_with_params(POST, MINT_INFO, self.MCS_API, params, self.token, None)

    def upload_file(self, file_path):
        params = {}
        if file_path:
            params['duration'] = '525'
            params['storage_copy'] = '5'

        files = [
            ('file', (
                file_path, open(file_path, 'rb')))
        ]
        return self._request_with_params(POST, UPLOAD_FILE, self.MCS_API, params, self.token, files)

    def stream_upload_file(self, wallet_address, file_path):
        params = {}
        if wallet_address:
            params['wallet_address'] = wallet_address
            params['duration'] = '525'
            params['storage_copy'] = '5'
            params['file'] = (file_path, open(file_path, 'rb'))
        return self._request_stream_upload(UPLOAD_FILE, self.MCS_API, params, self.token)

    def get_deal_detail(self, source_file_upload_id, deal_id='0'):
        params = {}
        if source_file_upload_id:
            params['source_file_upload_id'] = source_file_upload_id
        return self._request_with_params(GET, DEAL_DETAIL + deal_id, self.MCS_API, params, self.token, None)

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
        return self._request_with_params(POST, UPLOAD_FILE, self.MCS_API, params, self.token, files)
    
    def api_key_login(self, apikey, access_token, chain_name):
        params = {}
        params['apikey'] = apikey
        params['access_token'] = access_token
        params['network'] = chain_name
        result = self._request_with_params(POST, APIKEY_LOGIN, self.MCS_API, params, None, None)
        self.token = result['data']['jwt_token']