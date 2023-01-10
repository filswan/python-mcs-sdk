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


def test_get_buckets():
    info = test_info()
    api = BucketAPI(APIClient(info['api_key'], info['access_token'], chain_name))
    print(api.get_buckets())


def test_create_bucket():
    info = test_info()
    api = BucketAPI(APIClient(info['api_key'], info['access_token'], chain_name))
    print(api.create_bucket('test_bucket'))


def test_upload_file():
    info = test_info()
    api = BucketAPI(APIClient(info['api_key'], info['access_token'], chain_name))
    filepath = "/images/log_mcs.png"
    parentpath = os.path.abspath(os.path.dirname(__file__))
    api.upload_to_bucket(api.get_bucket_id('test_bucket'), parentpath + filepath)


def test_get_bucket_id():
    info = test_info()
    api = BucketAPI(APIClient(info['api_key'], info['access_token'], chain_name))
    print(api.get_bucket_id('test_bucket'))


def test_get_file_id():
    info = test_info()
    api = BucketAPI(APIClient(info['api_key'], info['access_token'], chain_name))
    print(api.get_file_id('test_bucket', 'log_mcs.png'))


def test_delete_bucket():
    info = test_info()
    api = BucketAPI(APIClient(info['api_key'], info['access_token'], chain_name))
    bucket_id = api.get_bucket_id('test_bucket')
    api.delete_bucket(bucket_id)


def test_upload_folder():
    info = test_info()
    api = BucketAPI(APIClient(info['api_key'], info['access_token'], chain_name))
    api.create_bucket('folder_bucket')
    api.upload_folder(api.get_bucket_id('folder_bucket'), os.path.abspath('test'))

def test_get_file_list():
    info = test_info()
    api = BucketAPI(APIClient(info['api_key'], info['access_token'], chain_name))
    api.get_file_list(api.get_bucket_id('folder_bucket'), 'test')
    api.get_full_file_list(api.get_bucket_id('folder_bucket'), 'test')

def test_download_file():
    info = test_info()
    api = BucketAPI(APIClient(info['api_key'], info['access_token'], chain_name))
    result = api.download_file(api.get_bucket_id('folder_bucket'), 'log_mcs.png', 'test/images')
    assert result == 'success'
    time.sleep(3)
    os.remove('log_mcs.png')