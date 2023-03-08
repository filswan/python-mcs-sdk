import pytest
import os
from dotenv import load_dotenv
from mcs.common.params import Params
from mcs import BucketAPI, APIClient
import time

def login():
    load_dotenv(".env_test")
    api_key = os.getenv('api_key')
    access_token = os.getenv('access_token')
    chain_name = os.getenv("chain_name")
    api = BucketAPI(APIClient(api_key, access_token, chain_name))
    
    assert api
    return api

def test_delete_bucket():
    api = login()
    print(api.delete_bucket('test-bucket'))

def test_list_buckets():
    api = login()
    assert api.list_buckets() is not None

def test_create_bucket():
    api = login()
    create = api.create_bucket('test-bucket')
    assert create == True

def test_get_bucket():
    api = login()
    bucket = api.get_bucket('test-bucket')
    assert bucket.bucket_name == 'test-bucket'


def test_create_folder():
    api = login()
    create = api.create_folder('test-bucket', 'folder1')

    assert create == True

# def test_create_folder_with_same_name():
#     api = login()
#     create = api.create_folder('test-bucket', 'folder1')
#     print(create)

def test_upload_file():
    api = login()
    filepath = "/images/log_mcs.png"
    parentpath = os.path.abspath(os.path.dirname(__file__))
    file = api.upload_file('test-bucket', "folder1/mcs-logo.png", parentpath + filepath)
    assert file.name == "mcs-logo.png"

def test_get_file():
    api = login()
    file = api.get_file('test-bucket', 'folder1/mcs-logo.png')

    assert file.name == "mcs-logo.png"


def test_get_file_list():
    api = login()
    list = api.list_files('test-bucket', 'folder1')
    
    assert len(list) == 1
    assert list[0].name == 'mcs-logo.png'


def test_download_file():
    api = login()
    result = api.download_file('test-bucket', 'folder1/mcs-logo.png', "aaaa.png")
    
    assert result == True


def test_delete_file():
    api = login()
    delete = api.delete_file('test-bucket', 'folder1/mcs-logo.png')

    assert delete == True

def test_upload_ipfs_folder():
    api = login()
    res = api.upload_ipfs_folder('test-bucket', 'ipfs-folder', 'images')

    print(res)