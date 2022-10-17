import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json
from mcs.common import utils, exceptions
from mcs.common import constants as c


class ApiClient(object):

    def _request(self, method, request_path, mcs_api, params, token, files=False):
        if method == c.GET:
            request_path = request_path + utils.parse_params_to_str(params)
        url = mcs_api + c.REST_API_VERSION + request_path
        header = {}
        if token:
            header["Authorization"] = "Bearer " + token
        print("url:", url)
        # send request
        response = None
        if method == c.GET:
            response = requests.get(url, headers=header)
        elif method == c.POST:
            if files:
                body = params
                print("body:", body)
                response = requests.post(url, data=body, headers=header, files=files)
            else:
                body = json.dumps(params) if method == c.POST else ""
                print("body:", body)
                response = requests.post(url, data=body, headers=header)
        elif method == c.DELETE:
            response = requests.delete(url, headers=header)

        # exception handle
        if not str(response.status_code).startswith('2'):
            raise exceptions.McsAPIException(response)

        return response.json()

    def _request_stream_upload(self, request_path, mcs_api, params, token):
        url = mcs_api + c.REST_API_VERSION + request_path
        header = {}
        if token:
            header["Authorization"] = "Bearer " + token
        print("url:", url)
        # send request
        response = None
        body = params
        print("body:", body)
        body = MultipartEncoder(body)
        header['Content-Type'] = body.content_type
        response = requests.post(url, data=body, headers=header)

        # exception handle
        if not str(response.status_code).startswith('2'):
            raise exceptions.McsAPIException(response)

        return response.json()

    def _request_without_params(self, method, request_path, mcs_api, token):
        return self._request(method, request_path, mcs_api, {}, token)

    def _request_with_params(self, method, request_path, mcs_api, params, token, files):
        return self._request(method, request_path, mcs_api, params, token, files)
