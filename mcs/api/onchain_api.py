from mcs.api_client import APIClient
from mcs.common.constants import *
import json


class OnchainAPI(object):
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = APIClient()
        self.api_client = api_client
        self.MCS_API = api_client.MCS_API
        self.token = self.api_client.token

    def get_payment_info(self, source_file_upload_id):
        params = {}
        if source_file_upload_id:
            params['source_file_upload_id'] = source_file_upload_id
        return self.api_client._request_with_params(GET, PAYMENT_INFO, self.MCS_API, params, self.token, None)

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
        return self.api_client._request_with_params(GET, TASKS_DEALS, self.MCS_API, params, self.token, None)

    def get_mint_info(self, source_file_upload_id, payload_cid, tx_hash, token_id, mint_address):
        params = {'source_file_upload_id': source_file_upload_id, 'payload_cid': payload_cid, 'tx_hash': tx_hash,
                  'token_id': int(token_id), 'mint_address': mint_address}
        return self.api_client._request_with_params(POST, MINT_INFO, self.MCS_API, params, self.token, None)

    def stream_upload_file(self, wallet_address, file_path):
        params = {}
        if wallet_address:
            params['wallet_address'] = wallet_address
            params['duration'] = '525'
            params['storage_copy'] = '5'
            params['file'] = (file_path, open(file_path, 'rb'))
        return self.api_client._request_stream_upload(UPLOAD_FILE, self.MCS_API, params, self.token)

    def get_deal_detail(self, source_file_upload_id, deal_id='0'):
        params = {}
        if source_file_upload_id:
            params['source_file_upload_id'] = source_file_upload_id
        return self.api_client._request_with_params(GET, DEAL_DETAIL + deal_id, self.MCS_API, params, self.token, None)

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
        return self.api_client._request_with_params(POST, UPLOAD_FILE, self.MCS_API, params, self.token, files)
