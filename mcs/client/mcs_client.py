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

    def api_key_login(self, apikey, access_token, chain_name):
        params = {}
        params['apikey'] = apikey
        params['access_token'] = access_token
        params['network'] = chain_name
        result = self._request_with_params(POST, APIKEY_LOGIN, self.MCS_API, params, None, None)
        self.token = result['data']['jwt_token']
