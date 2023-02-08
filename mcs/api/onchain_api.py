from mcs.api_client import APIClient
from mcs.common.constants import *
import json


class OnchainAPI(object):
    def __init__(self, api_client=None):
        '''Initialize Onchian API

        Parameter:
            :type api_client: obj APIClient
            :param api_client: The mcs api client object
        '''
        if api_client is None:
            api_client = APIClient()
        self.api_client = api_client
        self.MCS_API = api_client.MCS_API
        self.token = self.api_client.token

    def get_payment_info(self, source_file_upload_id):
        '''Get onchain upload payment information

        Parameters:
            :type source_file_upload_id: str
            :param source_file_upload_id: Source file upload id of file upload to Onchain upload

        Return:
            :type response: dict
            :return response: API response of payment information 
        '''
        params = {}
        if source_file_upload_id:
            params['source_file_upload_id'] = source_file_upload_id
        return self.api_client._request_with_params(GET, PAYMENT_INFO, self.MCS_API, params, self.token, None)

    def get_user_tasks_deals(self, page_number=None, page_size=None, file_name=None, status=None):
        '''Get deals and tasks information from Onchain

        Parameters:
            :type page_number: int
            :param page_number: The number of the page being returned

            :type page_size: int
            :param page_size: Size of the page being returned

            :type file_name: str
            :param file_name: Search with file name

            :type status: str
            :param status: Search with current status of the file

        Return:
            :type response: dict
            :return reponse: API response of list of deals uploaded to Onchain
        '''
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
        '''Update NFT mint information to Onchain storage
        
        Parameters:
            :type source_file_upload_id: str
            :param source_file_upload_id: Source file upload id of the file

            :type payload_cid: str
            :param payload_cid: Payload cid from IPFS server

            :type tx_hash: str
            :param tx_hash: Mint tx hash

            :type token_id: int
            :param token_id: Token id of the minted NFT

            :type mint_address: str
            :param mint_address: Mint contract address
        
        Return:
            :type response: dict
            :return response: NFT detail stored on Onchain storage
        '''
        params = {'source_file_upload_id': source_file_upload_id, 'payload_cid': payload_cid, 'tx_hash': tx_hash,
                  'token_id': int(token_id), 'mint_address': mint_address}
        return self.api_client._request_with_params(POST, MINT_INFO, self.MCS_API, params, self.token, None)

    def stream_upload_file(self, file_path):
        '''Stream upload file to Onchain storage

        Parameter:
            :type file_path: str
            :param file_path: Local file path for upload

        Return:
            :type response: dict
            :return response: Onchain storage upload API response
        '''
        params = {}
        params['duration'] = '525'
        params['storage_copy'] = '5'
        params['file'] = (file_path, open(file_path, 'rb'))
        return self.api_client._request_stream_upload(UPLOAD_FILE, self.MCS_API, params, self.token)

    def get_deal_detail(self, source_file_upload_id, deal_id='0'):
        '''Retrieve detailed information of a deal

        Parameters:
            :type source_file_upload_id: str
            :param source_file_upload_id: Source file upload id of the file

            :type deal_id: str
            :param deal_id: Deal id of the offline deal

        Return:
            :type response: dict
            :return response: Selected deal information
        '''
        params = {}
        if source_file_upload_id:
            params['source_file_upload_id'] = source_file_upload_id
        return self.api_client._request_with_params(GET, DEAL_DETAIL + deal_id, self.MCS_API, params, self.token, None)

    def upload_nft_metadata(self, address, file_name, image_url, tx_hash, size):
        '''Upload NFT metadata

        Parameters:
            :type address: str
            :param address: wallet address

            :type file_name: str
            :param file_name: file name for mint NFT

            :type image_url: str
            :param image_url: IPFS url of the file

            :type tx_hash: str
            :param tx_hash: Upload payment tx hash

            :type size: int
            :param size: Size of the file for mint

        Return:
            :type response: dict
            :return response: Onchain storage upload metadata API response
        '''
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
