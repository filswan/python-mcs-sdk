import shutil

import pytest
import requests_mock
from swan_mcs.common import constants as c

from swan_mcs import APIClient, BucketAPI
from dotenv import load_dotenv
import os
import datetime

from swan_mcs.object.bucket_storage import Bucket

abs_path = os.path.dirname(os.path.abspath(__file__))
load_dotenv(abs_path + '/.env')
api_key = os.getenv('api_key')
access_token = os.getenv('access_token')
chain_name = os.getenv('chain_name')
wrong_chain_name = os.getenv('wrong_chain_name')
wrong_api_key = os.getenv('wrong_api_key')
wrong_access_token = os.getenv('wrong_access_token')


@pytest.fixture()
def shared_mock_bucket(shared_mock_api_client):
    with requests_mock.Mocker() as m:
        m.get(c.GET_GATEWAY, json={'status': 'success', 'data': ['ipfs.io']})
        bucket_api = BucketAPI(shared_mock_api_client)
        return bucket_api


@pytest.fixture()
def shared_mock_api_client():
    with requests_mock.Mocker() as m:
        m.register_uri(c.POST, c.APIKEY_LOGIN, json={"data": {"jwt_token": "sample_token"}})
        api_client = APIClient(api_key="sample_api_key", access_token="sample_access_token",
                               chain_name="polygon.mumbai")
        return api_client


@pytest.fixture()
def shared_real_bucket():
    bucket = BucketAPI(APIClient(api_key, access_token, chain_name))
    return bucket


@pytest.fixture()
def shared_real_api_client():
    api_client = APIClient(api_key, access_token, chain_name)
    return api_client


@pytest.fixture()
def shared_login_info():
    return {
        "api_key": api_key,
        "access_token": access_token,
        "chain_name": chain_name,
        "wrong_chain_name": wrong_chain_name,
        "wrong_api_key": wrong_api_key,
        "wrong_access_token": wrong_access_token
    }


@pytest.fixture()
def shared_bucket_list():
    bucket_info = [
        {
            'bucket_name': 'test-bucket-1',
            'deleted_at': None,
            'bucket_uid': 'bucket_uid',
            'address': '0x5339595102d92a',
            'max_size': 34359738368,
            'size': 254,
            'is_free': True,
            'payment_tx': '',
            'is_active': True,
            'is_deleted': False,
            'file_number': 2,
            'id': 19,
            'created_at': '2023-01-05T19:00:01Z',
            'updated_at': '2023-01-05T19:00:01Z',
        },
        {
            'bucket_name': 'test-bucket-2',
            'deleted_at': None,
            'bucket_uid': 'db069404-f846-3wasdf',
            'address': '0x5asdfsadfadsfaewf2d92a',
            'max_size': 34359738368,
            'size': 2524,
            'is_free': True,
            'payment_tx': '',
            'is_active': True,
            'is_deleted': False,
            'file_number': 22,
            'id': 191,
            'created_at': '2023-01-05T19:00:01Z',
            'updated_at': '2023-01-05T19:00:01Z', }]
    return bucket_info


@pytest.fixture()
def shared_file_list():
    file_info = [
        {
            'name': "test-file-name-1",
            'address': "simple_address",
            'bucket_uid': "simple_bucket_uid",
            'created_at': "2023-03-28T20:09:45Z",
            'deleted_at': None,
            'file_hash': "simple_file_hash",
            'id': 12345,
            'is_deleted': False,
            'is_folder': False,
            'object_name': "test-object-1",
            'payload_cid': "simple_payload_cid",
            'pin_status': "Pinned",
            'prefix': "",
            'size': 244029,
            'type': 2,
            'updated_at': "2023-03-28T20:09:45Z"
        },
        {
            'name': "IMG_1708-1.JPG",
            'address': "simple_address-1",
            'bucket_uid': "simple_bucket_uid-1",
            'created_at': "2023-03-28T20:09:45Z",
            'deleted_at': None,
            'file_hash': "simple_file_hash-1",
            'id': 1234567,
            'is_deleted': False,
            'is_folder': False,
            'object_name': "IMG_1708-1.JPG",
            'payload_cid': "simple_payload_cid-1",
            'pin_status': "Pinned",
            'prefix': "",
            'size': 244029,
            'type': 2,
            'updated_at': "2023-03-28T20:09:45Z",
        }]
    return file_info


@pytest.fixture()
def shared_current_time():
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S.%f")
    return current_time


@pytest.fixture()
def shared_temp_file():
    files = [
        {'name': 'file1.txt', 'size': 10, 'content': b'HelloWorld'},
        {'name': 'file2.txt', 'size': 20, 'content': b'ThisIsATest'}
    ]
    return files


@pytest.fixture()
def shared_ipfs_file_list():
    ipfs_info = [
        {

            "name": "test_ipfs_file_name-1",
            "address": "test_address-1",
            "prefix": "",
            "bucket_uid": "test_bucket_uid-1",
            "file_hash": "",
            "size": 1080,
            "payload_cid": "test_payload_cid-1",
            "pin_status": "Pinned",
            "is_deleted": False,
            "is_folder": False,
            "object_name": "test",
            "type": 0,
            "id": 1,
            "created_at": "2023-04-10T20:35:47.990049944Z",
            "updated_at": "2023-04-10T20:35:47.990049944Z",
            "deleted_at": None

        },
        {

            "name": "test_ipfs_file_name-2",
            "address": "test_address-2",
            "prefix": "",
            "bucket_uid": "test_bucket_uid-2",
            "file_hash": "",
            "size": 10800000,
            "payload_cid": "test_payload_cid-2",
            "pin_status": "Pinned",
            "is_deleted": False,
            "is_folder": False,
            "object_name": "test",
            "type": 0,
            "id": 2,
            "created_at": "2023-04-10T20:35:47.990049944Z",
            "updated_at": "2023-04-10T20:35:47.990049944Z",
            "deleted_at": None

        }
    ]
    return ipfs_info


@pytest.fixture(scope="function", autouse=True)
def remove_temp_dir():
    if os.path.exists(os.path.join(os.getcwd(), "test_dir")):
        shutil.rmtree(os.path.join(os.getcwd(), "test_dir"))


@pytest.fixture(scope="function", autouse=True)
def temp_dir():
    dirpath = os.path.join(os.getcwd(), "test_dir")
    os.makedirs(dirpath)
    yield dirpath
    # teardown - remove directory after all tests complete
    shutil.rmtree(dirpath)


@pytest.fixture(scope="module", autouse=True)
def delete_all_buckets():
    bucket_api = BucketAPI(APIClient(api_key, access_token, chain_name))
    buckets = bucket_api.list_buckets()
    for bucket in buckets:
        bucket_api.delete_bucket(bucket.bucket_name)
        print("Deleted bucket: ", bucket.bucket_name)


def pytest_sessionfinish(session, exitstatus):
    delete_all_buckets()