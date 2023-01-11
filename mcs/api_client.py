from mcs.common.constants import *
from mcs.common.params import Params
import requests
import json
from mcs.common import utils, exceptions
from mcs.common import constants as c
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
from tqdm import tqdm
from pathlib import Path


class APIClient(object):
    def __init__(self, api_key, access_token, chain_name=None):
        self.token = None
        if chain_name is None:
            chain_name = "polygon.mainnet"
        self.chain_name = chain_name
        self.api_key = api_key
        self.access_token = access_token
        self.MCS_API = Params(self.chain_name).MCS_API
        if api_key and access_token:
            self.api_key_login()
        self.CHAIN_NAME = self.get_params()['data']['chain_name']
        self.SWAN_PAYMENT_ADDRESS = self.get_params()['data']['payment_contract_address']
        self.USDC_TOKEN = self.get_params()['data']['usdc_address']
        self.MINT_ADDRESS = self.get_params()['data']['mint_contract_address']

    def get_params(self):
        return self._request_without_params(GET, MCS_PARAMS, self.MCS_API, self.token)

    def get_price_rate(self):
        return self._request_without_params(GET, PRICE_RATE, self.MCS_API, self.token)

    def api_key_login(self):
        params = {}
        params['apikey'] = self.api_key
        params['access_token'] = self.access_token
        params['network'] = self.chain_name
        result = self._request_with_params(POST, APIKEY_LOGIN, self.MCS_API, params, None, None)
        self.token = result['data']['jwt_token']
        return self.token

    def _request(self, method, request_path, mcs_api, params, token, files=False):
        if method == c.GET:
            request_path = request_path + utils.parse_params_to_str(params)
        url = mcs_api + request_path
        header = {}
        if token:
            header["Authorization"] = "Bearer " + token
        # send request
        response = None
        if method == c.GET:
            response = requests.get(url, headers=header)
        elif method == c.PUT:
            body = json.dumps(params)
            response = requests.put(url, data=body, headers=header)
        elif method == c.POST:
            if files:
                body = params
                response = requests.post(url, data=body, headers=header, files=files)
            else:
                body = json.dumps(params) if method == c.POST else ""
                response = requests.post(url, data=body, headers=header)
        elif method == c.DELETE:
            if params:
                body = json.dumps(params)
                response = requests.delete(url, data=body, headers=header)
            else:
                response = requests.delete(url, headers=header)

        # exception handle
        if not str(response.status_code).startswith('2'):
            raise exceptions.McsAPIException(response)
        json_res = response.json()
        if str(json_res['status']) == 'error':
            raise exceptions.McsRequestException(json_res['message'])

        return response.json()

    def _request_stream_upload(self, request_path, mcs_api, params, token):
        url = mcs_api + request_path
        header = {}
        if token:
            header["Authorization"] = "Bearer " + token
        # send request
        path = Path(params['file'][0])
        size = path.stat().st_size
        filename = path.name
        with tqdm(
            desc=filename,
            total=size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            encode = MultipartEncoder(params)
            body = MultipartEncoderMonitor(
                encode, lambda monitor: bar.update(monitor.bytes_read - bar.n)
            )
            header['Content-Type'] = body.content_type
            response = requests.post(url, data=body, headers=header)

        # exception handle
        if not str(response.status_code).startswith('2'):
            raise exceptions.McsAPIException(response)
        json_res = response.json()
        if str(json_res['status']) == 'error':
            raise exceptions.McsRequestException(json_res['message'])

        return response.json()

    def _request_bucket_upload(self, request_path, mcs_api, params, token):
        url = mcs_api + request_path
        header = {}
        if token:
            header["Authorization"] = "Bearer " + token
        # send request
        encode = MultipartEncoder(params)
        previous = Previous()
        body = MultipartEncoderMonitor(
                encode, lambda monitor: self.bar.update(previous.update(monitor.bytes_read)),
            )
        header['Content-Type'] = body.content_type
        response = requests.post(url, data=body, headers=header)

        # exception handle
        if not str(response.status_code).startswith('2'):
            raise exceptions.McsAPIException(response)
        json_res = response.json()
        if str(json_res['status']) == 'error':
            raise exceptions.McsRequestException(json_res['message'])

        return response.json()
    
    def upload_progress_bar(self, file_name, file_size):
        self.bar = tqdm(desc=file_name, total=file_size, unit='B', unit_scale=True, unit_divisor=1024)

    def _request_without_params(self, method, request_path, mcs_api, token):
        return self._request(method, request_path, mcs_api, {}, token)

    def _request_with_params(self, method, request_path, mcs_api, params, token, files):
        return self._request(method, request_path, mcs_api, params, token, files)

class Previous():
    def __init__(self):
        self.previous = 0
    
    def update(self, new):
        self.old = self.previous
        self.previous = new
        return self.previous - self.old