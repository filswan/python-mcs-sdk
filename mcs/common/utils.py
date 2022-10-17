import requests
from mcs.common.constants import FIL_PRICE_API
import json
import os


def get_fil_price():
    response = requests.request("GET", FIL_PRICE_API)
    price = response.json()["data"]['historical_average_price_verified']
    price = float(str.split(price)[0]) / 1024 / 1024 / 1024 / 1e8
    return price


def parse_params_to_str(params):
    url = '?'
    for key, value in params.items():
        url = url + str(key) + '=' + str(value) + '&'
    return url[0:-1]


def get_amount(size, rate):
    fil_price = get_fil_price()
    amount = fil_price * size * 525 / 365 * rate
    if amount == 0:
        amount = 0.000002
    return amount


def get_contract_abi(abi_name):
    parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/contract/abi/"
    with open(parent_path + abi_name, 'r') as abi_file:
        abi_data = json.load(abi_file)
        return json.dumps(abi_data)
