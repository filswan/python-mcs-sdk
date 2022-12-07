from mcs.api.mcs_api import McsAPI

import web3
from eth_account import Account
from eth_account.messages import encode_defunct
from mcs import ApiClient
from mcs.common.constants import *
import json

import os
import time
import urllib.request

class MetaSpaceAPI(McsAPI):

    def __init__(self, mcs_url, meta_url=None):
        self.MCS_API = mcs_url
        if meta_url:
            self.MetaSpace_API = meta_url
        else: self.MetaSpace_API = METASPACE_API
        self.token = None
    
    def get_buckets(self):
        return self._request_without_params(GET, DIRECTORY, self.MetaSpace_API, self.token)
    
    def get_bucket_info(self, bucket_name):
        if self.special_char(bucket_name):
            return "Name cannot contain space and special characters"
        return self._request_without_params(GET, DIRECTORY + '/{}'.format(bucket_name), self.MetaSpace_API, self.token)
    
    def get_bucket_id(self, bucket_name):
        if self.special_char(bucket_name):
            return "Name cannot contain space and special characters"
        buckets = self.get_buckets()['data']['objects']
        for bucket in buckets:
            if bucket['name'] == bucket_name:
                return bucket['id']
        return None
    
    def get_file_id(self, bucket_name, file_name):
        if self.special_char(bucket_name+file_name):
            return "Name cannot contain space and special characters"
        files = self.get_bucket_info(bucket_name)['data']['objects']
        for file in files:
            if file['name'] == file_name:
                return file['id']
        return None

    def create_bucket(self, bucket_name):
        if self.special_char(bucket_name):
            return "Name cannot contain space and special characters"
        params = {}
        params['path'] = '/{}'.format(bucket_name)
        return self._request_with_params(PUT, DIRECTORY, self.MetaSpace_API, params, self.token, None)

    # delete directory use its id
    def delete_bucket(self, dirs):
        params = {}
        params['items'] = []
        params['dirs'] = dirs
        if type(dirs) != list:
            params['dirs'] = [str(dirs)]
        return self._request_with_params(DELETE, DELETE_OBJECT, self.MetaSpace_API, params, self.token, None)

    def create_upload_session(self, bucket_name, file_name, file_path):
        if self.special_char(bucket_name+file_name):
            return "Name cannot contain space and special characters"
        bucket_info = self.get_bucket_info(bucket_name)
        params = {}
        params['path'] = '/{}'.format(bucket_name)
        params['size'] = os.stat(file_path).st_size
        params['name'] = file_name
        params['policy_id'] = bucket_info['data']['policy']['id']
        params['last_modified'] = int(time.time())
        return self._request_with_params(PUT, UPLOAD_SESSION, self.MetaSpace_API, params, self.token, None)

    def upload_to_bucket(self, bucket_name, file_name, file_path):
        if self.special_char(bucket_name+file_name):
            return "Name cannot contain space and special characters"
        if os.stat(file_path).st_size == 0:
            return "Please upload a file larger than 0byte."
        session = self.create_upload_session(bucket_name, file_name, file_path)['data']['sessionID']
        params = {}
        params= open(file_path, 'rb')
        return self._request_upload(UPLOAD_SESSION+'/{}/0'.format(session), self.MetaSpace_API, params, self.token)

    def delete_from_bucket(self, items):
        params = {}
        params['items'] = items
        params['dirs'] = []
        if type(items) != list:
            params['items'] = [str(items)]
        return self._request_with_params(DELETE, DELETE_OBJECT, self.MetaSpace_API, params, self.token, None)
    
    def special_char(self, line):
        special_characters = "!@#$%^&*()-+?=,<>/\'\" \n\t\v\f\r"

        if any(c in special_characters for c in line):
            return True
        return False

    def download_file(self, bucket_name, file_name):
        objects = self.get_bucket_info(bucket_name)['data']['objects']
        for object in objects:
            if object['name']==file_name:
                url = object['ipfs_url']
                break
        name = url.split('?filename=')[-1]
        with open(name, 'wb') as f:
            data = urllib.request.urlopen(url)
            f.write(data.read())