from mcs.api_client import APIClient
from mcs.object.onchain_storage import PaymentInfo, SourceFile
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
        if source_file_upload_id:
            params = {'source_file_upload_id' : source_file_upload_id}
            result = self.api_client._request_with_params(GET, PAYMENT_INFO, self.MCS_API, params, self.token, None)
            if result['status'] != 'success':
                print("\033[31mError: " + result['message'] + "\033[0m" )
                return
            return PaymentInfo(result['data'])
        print("\033[31mError: source file id is None\033[0m")
        return 

    def get_user_tasks_deals(self):
        params = {'page_size' : 10}
        result = self.api_client._request_with_params(GET, TASKS_DEALS, self.MCS_API, params, self.token, None)
        if result['status'] != 'success':
            print("\033[31mError: " + result['message'] + "\033[0m" )
            return
        total_count = result['data']['total_record_count']
        sourcefiles = []
        for i in range(total_count//10 + 1):
            params['page_number'] = i+1
            result = self.api_client._request_with_params(GET, TASKS_DEALS, self.MCS_API, params, self.token, None)
            for i in result['data']['source_file_upload']:
                sourcefiles.append(SourceFile(i))
        return sourcefiles

    def get_mint_info(self, source_file_upload_id, payload_cid, tx_hash, token_id, mint_address):
        params = {'source_file_upload_id': source_file_upload_id, 'payload_cid': payload_cid, 'tx_hash': tx_hash,
                  'token_id': int(token_id), 'mint_address': mint_address}
        return self.api_client._request_with_params(POST, MINT_INFO, self.MCS_API, params, self.token, None)

    def stream_upload_file(self, file_path):
        if file_path:
            params = {'duration' : '525', 'storage_copy' : '5', 'file' : (file_path, open(file_path, 'rb'))}
            result = self.api_client._request_stream_upload(UPLOAD_FILE, self.MCS_API, params, self.token)
            if result['status'] != 'success':
                print("\033[31mError: " + result['message'] + "\033[0m" )
                return
            return SourceFile(result['data'])
        print("\033[31mError: file path is None\033[0m")
        return 

    def get_deal_detail(self, source_file_upload_id, deal_id='0'):
        if source_file_upload_id:
            params = {'source_file_upload_id' : source_file_upload_id}
            return self.api_client._request_with_params(GET, DEAL_DETAIL + deal_id, self.MCS_API, params, self.token, None)
        print("\033[31mError: source file upload id is None\033[0m")
        return

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
        result =  self.api_client._request_with_params(POST, UPLOAD_FILE, self.MCS_API, params, self.token, files)
        if result['status'] != 'success':
            print("\033[31mError: " + result['message'] + "\033[0m" )
            return
        return result['data']
