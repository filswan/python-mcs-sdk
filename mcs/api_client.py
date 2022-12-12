import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
import json
from mcs.common import utils, exceptions
from mcs.common import constants as c
from tqdm import tqdm
from pathlib import Path


class ApiClient(object):

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
            else :
                response = requests.delete(url, headers=header)

        # exception handle
        if not str(response.status_code).startswith('2'):
            raise exceptions.McsAPIException(response)
        json_res = response.json()
        if str(json_res['status']) == 'error':
            raise exceptions.McsRequestException(json_res['message'])

        return response.json()

    def _request_upload(self, request_path, mcs_api, params, token):
        url = mcs_api + request_path
        header = {}
        if token:
            header["Authorization"] = "Bearer " + token
        response = requests.post(url, data=params, headers=header)

        # exception handle
        if not str(response.status_code).startswith('2'):
            raise exceptions.McsAPIException(response)

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

    def _request_without_params(self, method, request_path, mcs_api, token):
        return self._request(method, request_path, mcs_api, {}, token)

    def _request_with_params(self, method, request_path, mcs_api, params, token, files):
        return self._request(method, request_path, mcs_api, params, token, files)
