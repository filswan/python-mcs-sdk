import pytest
import os
from dotenv import load_dotenv
from mcs.common.params import Params
from mcs.client import BucketClient


chain_name = "polygon.mumbai"
metaspace = 'https://calibration-mybucket-api.filswan.com/api/'

def test_info():
    load_dotenv(".env_test")
    wallet_info = {
        'wallet_address': os.getenv('wallet_address'),
        'private_key': os.getenv('private_key'),
        'rpc_endpoint': os.getenv('rpc_endpoint'),
        'api_key': os.getenv('api_key'),
        'access_token': os.getenv('access_token')
    }
    return wallet_info

def test_user_register():
    info = test_info()
    api = BucketClient(Params(chain_name).MCS_API)
    jwt_token = api.api_key_login(info['api_key'], info['access_token'], chain_name)
    print(jwt_token)


def test_get_buckets():
    info = test_info()
    api = BucketClient(Params(chain_name).MCS_API)
    api.api_key_login(info['api_key'], info['access_token'], chain_name)
    print(api.get_buckets())


def test_create_bucket():
    info = test_info()
    api = BucketClient(Params(chain_name).MCS_API)
    api.api_key_login(info['api_key'], info['access_token'], chain_name)
    print(api.create_bucket('test_bucket'))


def test_upload_file():
    info = test_info()
    api = BucketClient(Params(chain_name).MCS_API)
    filepath = "/images/log_mcs.png"
    parentpath = os.path.abspath(os.path.dirname(__file__))
    api.api_key_login(info['api_key'], info['access_token'], chain_name)
    api.upload_to_bucket(api.get_bucket_id('test_bucket'), parentpath+filepath)
    

def test_get_bucket_id():
    info = test_info()
    api = BucketClient(Params(chain_name).MCS_API)
    api.api_key_login(info['api_key'], info['access_token'], chain_name)
    print(api.get_bucket_id('test_bucket'))


def test_get_file_id():
    info = test_info()
    api = BucketClient(Params(chain_name).MCS_API)
    api.api_key_login(info['api_key'], info['access_token'], chain_name)
    print(api.get_file_id('test_bucket', 'log_mcs.png'))


def test_delete_bucket():
    info = test_info()
    api = BucketClient(Params(chain_name).MCS_API)
    api.api_key_login(info['api_key'], info['access_token'], chain_name)
    bucket_id = api.get_bucket_id('test_bucket')
    api.delete_bucket(bucket_id)

def test_upload_folder():
    info = test_info()
    api = BucketClient(Params(chain_name).MCS_API)
    api.api_key_login(info['api_key'], info['access_token'], chain_name)
    api.create_bucket('folder_bucket')
    api.upload_folder(api.get_bucket_id('folder_bucket'), os.path.abspath('test'))