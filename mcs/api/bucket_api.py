from mcs.api.mcs_api import McsAPI
from mcs.common.constants import *

from hashlib import md5
import os

class BucketAPI(McsAPI):

    def get_buckets(self):
        return self._request_without_params(GET, BUCKET_LIST, self.MCS_API, self.token)

    def create_bucket(self, bucket_name):
        params = {}
        params['bucket_name'] = bucket_name
        return self._request_with_params(POST, CREATE_BUCKET, self.MCS_API, params, self.token, None)
    
    def delete_bucket(self, bucket_id):
        params = {}
        params['bucket_uid'] = bucket_id
        return self._request_with_params(GET, DELETE_BUCKET, self.MCS_API, params, self.token, None)
    
    def get_file_info(self, file_id):
        params = {}
        params['file_id'] = file_id
        return self._request_with_params(GET, FILE_INFO, self.MCS_API, params, self.token, None)

    def create_folder(self, file_name, prefix, bucket_id):
        params = {}
        params["file_name"] = file_name
        params["prefix"] = prefix
        params["bucket_uid"] = bucket_id
        return self._request_with_params(POST, CREATE_FOLDER, self.MCS_API, params, self.token, None)
    
    def delete_file(self, file_id):
        params = {}
        params['file_id'] = file_id
        return self._request_with_params(GET, DELETE_FILE, self.MCS_API, params, self.token, None)

    def get_file_list(self, prefix, bucket_id, limit=10, offset=0):
        params = {}
        params['bucket_uid'] = bucket_id
        params['prefix'] = prefix
        params['limit'] = limit
        params['offset'] = offset
        return self._request_with_params(GET, FILE_LIST, self.MCS_API, params, self.token, None)

    def check_file(self, bucket_id, file_hash, file_name, prefix):
        params = {}
        params['bucket_uid'] = bucket_id
        params['file_hash'] = file_hash
        params['file_name'] = file_name
        params['prefix'] = prefix
        return self._request_with_params(POST, CHECK_UPLOAD, self.MCS_API, params, self.token, None)

    def upload_chunk(self, file_hash, file_name, chunk):
        params = {}
        params['hash'] = file_hash
        params['file'] = (file_name, chunk)
        return self._request_bucket_upload(UPLOAD_CHUNK, self.MCS_API, params, self.token)
    
    def merge_file(self, bucket_id, file_hash, file_name, prefix):
        params = {}
        params['bucket_uid'] = bucket_id
        params['file_hash'] = file_hash
        params['file_name'] = file_name
        params['prefix'] = prefix
        return self._request_with_params(POST, MERGE_FILE, self.MCS_API, params, self.token, None)
    
    def read_chunks(self, file, chunk_size=10485760):
        while True:
            data = file.read(chunk_size)
            if not data:
                break
            yield data

    def upload_to_bucket(self, bucket_id, file_path):
        file_name = os.path.basename(file_path)
        with open(file_path, 'rb') as file:
            file_hash = md5(file.read()).hexdigest()
        result = self.check_file(bucket_id, file_hash, file_name, '')
        if not (result['data']['file_is_exist']):
            with open(file_path, 'rb') as file:
                i = 0
                for chunk in self.read_chunks(file):
                    i+= 1
                    self.upload_chunk(file_hash, str(i)+'_'+file_name, chunk)
                file.close()
            if not (result['data']['ipfs_is_exist']):
                self.merge_file(bucket_id, file_hash, file_name, '')
        else: 
            print('File already existed')

