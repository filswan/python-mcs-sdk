from mcs.api.mcs_api import McsAPI
from mcs.common.constants import *

from hashlib import md5
from queue import Queue
import os, threading

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

    def create_folder(self, file_name, bucket_id, prefix=''):
        params = {}
        params["file_name"] = file_name
        params["prefix"] = prefix
        params["bucket_uid"] = bucket_id
        return self._request_with_params(POST, CREATE_FOLDER, self.MCS_API, params, self.token, None)
    
    def delete_file(self, file_id):
        params = {}
        params['file_id'] = file_id
        return self._request_with_params(GET, DELETE_FILE, self.MCS_API, params, self.token, None)

    def get_file_list(self, bucket_id, prefix='', limit=10, offset=0):
        params = {}
        params['bucket_uid'] = bucket_id
        params['prefix'] = prefix
        params['limit'] = limit
        params['offset'] = offset
        return self._request_with_params(GET, FILE_LIST, self.MCS_API, params, self.token, None)

    def check_file(self, bucket_id, file_hash, file_name, prefix=''):
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
    
    def thread_upload_chunk(self, queue, file_hash, file_name):
        while not queue.empty():
            chunk = queue.get()
            self.upload_chunk(file_hash, chunk[0]+'_'+file_name, chunk[1])
    
    def merge_file(self, bucket_id, file_hash, file_name, prefix=''):
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

    def upload_to_bucket(self, bucket_id, file_path, prefix=''):
        file_name = os.path.basename(file_path)
        with open(file_path, 'rb') as file:
            file_hash = md5(file.read()).hexdigest()
        result = self.check_file(bucket_id, file_hash, file_name, prefix)
        if not (result['data']['file_is_exist']):
            with open(file_path, 'rb') as file:
                i = 0
                queue = Queue()
                for chunk in self.read_chunks(file):
                    i+= 1
                    queue.put((str(i), chunk))
                file.close()
            for i in range(3):
                worker = threading.Thread(target=self.thread_upload_chunk, args=(queue, file_hash, file_name))
                worker.start()
            if not (result['data']['ipfs_is_exist']):
                self.merge_file(bucket_id, file_hash, file_name, prefix)
        else: 
            print('File already existed')

    def upload_folder(self, bucket_id, folder_path, prefix=''):
        path = os.path.basename(folder_path)
        folder_name = os.path.splitext(path)[0]
        self.create_folder(folder_name, bucket_id, prefix)
        files = os.listdir(folder_path)
        success = []
        for f in files:
            f_path = os.path.join(folder_path,f)
            if os.path.isdir(f_path):
                success.extend(self.upload_folder(bucket_id, f_path, os.path.join(prefix,folder_name)))
            else:
                self.upload_to_bucket(bucket_id, f_path, os.path.join(prefix,folder_name))
                success.append(f_path)
        return success
