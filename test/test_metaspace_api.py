import pytest
import os
from dotenv import load_dotenv
from mcs.common.params import Params
from mcs.api import McsAPI
from mcs.api import MetaSpaceAPI


chain_name = "main"

def test_info():
    load_dotenv(".env_" + chain_name)
    wallet_info = {
        'wallet_address': os.getenv('wallet_address'),
        'private_key': os.getenv('private_key'),
        'rpc_endpoint': os.getenv('rpc_endpoint'),
    }
    return wallet_info


def test_user_register():
    info = test_info()
    api = MetaSpaceAPI(Params(chain_name).MCS_API)
    jwt_token = api.get_jwt_token(info['wallet_address'], info['private_key'], "polygon.mainnet")
    print(jwt_token)


def test_get_buckets():
    info = test_info()
    api = MetaSpaceAPI(Params(chain_name).MCS_API)
    api.get_jwt_token(info['wallet_address'], info['private_key'], "polygon.mainnet")
    print(api.get_buckets())


def test_create_bucket():
    info = test_info()
    api = MetaSpaceAPI(Params(chain_name).MCS_API)
    api.get_jwt_token(info['wallet_address'], info['private_key'], "polygon.mainnet")
    print(api.create_bucket('test_bucket'))


def test_bucket_info():
    info = test_info()
    api = MetaSpaceAPI(Params(chain_name).MCS_API)
    api.get_jwt_token(info['wallet_address'], info['private_key'], "polygon.mainnet")
    print(api.get_bucket_info('test_bucket'))

def test_upload_file():
    info = test_info()
    api = MetaSpaceAPI(Params(chain_name).MCS_API)
    filepath = "/images/0bFile.txt"
    parentpath = os.path.abspath(os.path.dirname(__file__))
    api.get_jwt_token(info['wallet_address'], info['private_key'], "polygon.mainnet")
    upload = api.upload_to_bucket('test_bucket', 'mcs_logo', parentpath+filepath)
    

def test_get_bucket_id():
    info = test_info()
    api = MetaSpaceAPI(Params(chain_name).MCS_API)
    api.get_jwt_token(info['wallet_address'], info['private_key'], "polygon.mainnet")
    print(api.get_bucket_id('test_bucket'))


def test_get_file_id():
    info = test_info()
    api = MetaSpaceAPI(Params(chain_name).MCS_API)
    api.get_jwt_token(info['wallet_address'], info['private_key'], "polygon.mainnet")
    print(api.get_file_id('test_bucket', 'mcs_logo'))


def test_delete_bucket():
    info = test_info()
    api = MetaSpaceAPI(Params(chain_name).MCS_API)
    jwt_token = api.get_jwt_token(info['wallet_address'], info['private_key'], "polygon.mainnet")
    buckets = api.get_buckets()['data']['objects']
    for i in buckets:
        if i['name'] == 'test_bucket':
            api.delete_bucket(i['id'])