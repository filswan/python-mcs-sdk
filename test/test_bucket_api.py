import pytest
import os
from dotenv import load_dotenv
from mcs.common.params import Params
from mcs import BucketAPI, APIClient
import time

chain_name = "polygon.mumbai"


def test_info():
    load_dotenv(".env_test")
    wallet_info = {
        'api_key': os.getenv('api_key'),
        'access_token': os.getenv('access_token')
    }
    return wallet_info


def test_user_register():
    info = test_info()
    api = BucketAPI(APIClient(info['api_key'], info['access_token'], chain_name))
    print(api.token)


def test_list_buckets():
    info = test_info()
    api = BucketAPI(APIClient(info['api_key'], info['access_token'], chain_name))
    for i in api.list_buckets():
        print(i.to_json())


def test_create_bucket():
    info = test_info()
    api = BucketAPI(APIClient(info['api_key'], info['access_token'], chain_name))
    print(api.create_bucket('33333'))


def test_delete_bucket():
    info = test_info()
    api = BucketAPI(APIClient(info['api_key'], info['access_token'], chain_name))
    print(api.delete_bucket('33333'))


def test_get_bucket():
    info = test_info()
    api = BucketAPI(APIClient(info['api_key'], info['access_token'], chain_name))
    print(api.get_bucket('123121'))


def test_create_folder():
    info = test_info()
    api = BucketAPI(APIClient(info['api_key'], info['access_token'], chain_name))
    print(api.create_folder('12312', '55555', '44444'))


def test_delete_file():
    info = test_info()
    api = BucketAPI(APIClient(info['api_key'], info['access_token'], chain_name))
    print(api.delete_file('12312', '44444/55555/log_mcs.png'))


def test_upload_file():
    info = test_info()
    api = BucketAPI(APIClient(info['api_key'], info['access_token'], chain_name))
    filepath = "/images/log_mcs.png"
    parentpath = os.path.abspath(os.path.dirname(__file__))
    print(api.upload_file('12312', "44444/55555/log_mcs.png", parentpath + filepath).to_json())


def test_get_file():
    info = test_info()
    api = BucketAPI(APIClient(info['api_key'], info['access_token'], chain_name))
    print(api.get_file('12312', '44444/55555/log_mcs.png').to_json())


def test_get_file_list():
    info = test_info()
    api = BucketAPI(APIClient(info['api_key'], info['access_token'], chain_name))
    for i in api.list_files(12312, '44444/55555', 100, '0'):
        print(i.to_json())


def test_download_file():
    info = test_info()
    api = BucketAPI(APIClient(info['api_key'], info['access_token'], chain_name))
    result = api.download_file('12312', '44444/55555/log_mcs.png', "aaaa.png")
    print(result)
