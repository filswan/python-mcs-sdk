from mcs.api_client import APIClient
from mcs.common.constants import *
from hashlib import md5
from queue import Queue
import os, threading, time
import urllib.request


class BucketAPI(object):
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = APIClient()
        self.api_client = api_client
        self.MCS_API = api_client.MCS_API
        self.token = self.api_client.token

    def get_buckets(self):
        return self.api_client._request_without_params(GET, BUCKET_LIST, self.MCS_API, self.token)

    def create_bucket(self, bucket_name):
        params = {'bucket_name': bucket_name}
        return self.api_client._request_with_params(POST, CREATE_BUCKET, self.MCS_API, params, self.token, None)

    def delete_bucket(self, bucket_id):
        params = {'bucket_uid': bucket_id}
        return self.api_client._request_with_params(GET, DELETE_BUCKET, self.MCS_API, params, self.token, None)

    def get_bucket_id(self, bucket_name):
        bucketlist = self.get_buckets()['data']
        for bucket in bucketlist:
            if bucket['BucketName'] == bucket_name:
                return bucket['BucketUid']
        return None

    def get_file_info(self, file_id):
        params = {'file_id': file_id}
        return self.api_client._request_with_params(GET, FILE_INFO, self.MCS_API, params, self.token, None)

    def create_folder(self, folder_name, bucket_id, prefix=''):
        params = {"file_name": folder_name, "prefix": prefix, "bucket_uid": bucket_id}
        return self.api_client._request_with_params(POST, CREATE_FOLDER, self.MCS_API, params, self.token, None)

    def delete_file(self, file_id):
        params = {'file_id': file_id}
        return self.api_client._request_with_params(GET, DELETE_FILE, self.MCS_API, params, self.token, None)

    def get_file_list(self, bucket_id, prefix='', limit=10):
        params = {'bucket_uid': bucket_id, 'prefix': prefix, 'limit': limit, 'offset': 0}
        count = self.api_client._request_with_params(GET, FILE_LIST, self.MCS_API, params, self.token, None)['data'][
            'Count']
        result = {}
        for i in range(count // 10 + 1):
            params['offset'] = i
            result['Page{}'.format(i + 1)] = \
                self.api_client._request_with_params(GET, FILE_LIST, self.MCS_API, params, self.token, None)['data'][
                    'FileList']
        return result

    def get_full_file_list(self, bucket_id, prefix=''):
        params = {'bucket_uid': bucket_id, 'prefix': prefix, 'limit': 100, 'offset': 0}
        count = self.api_client._request_with_params(GET, FILE_LIST, self.MCS_API, params, self.token, None)['data'][
            'Count']
        result = []
        for i in range(count // 10 + 1):
            params['offset'] = i
            result.extend(
                self.api_client._request_with_params(GET, FILE_LIST, self.MCS_API, params, self.token, None)['data'][
                    'FileList'])
        return result

    def get_file_id(self, bucket_name, file_name, prefix=''):
        filelist = self.get_full_file_list(self.get_bucket_id(bucket_name), prefix)
        for file in filelist:
            if file['Name'] == file_name and not file['IsFolder']:
                return file['ID']
        return None

    def check_file(self, bucket_id, file_hash, file_name, prefix=''):
        params = {'bucket_uid': bucket_id, 'file_hash': file_hash, 'file_name': file_name, 'prefix': prefix}
        return self.api_client._request_with_params(POST, CHECK_UPLOAD, self.MCS_API, params, self.token, None)

    def upload_chunk(self, file_hash, file_name, chunk):
        params = {'hash': file_hash, 'file': (file_name, chunk)}
        return self.api_client._request_bucket_upload(UPLOAD_CHUNK, self.MCS_API, params, self.token)

    def thread_upload_chunk(self, queue, file_hash, file_name):
        while not queue.empty():
            chunk = queue.get()
            self.upload_chunk(file_hash, chunk[0] + '_' + file_name, chunk[1])

    def merge_file(self, bucket_id, file_hash, file_name, prefix=''):
        params = {'bucket_uid': bucket_id, 'file_hash': file_hash, 'file_name': file_name, 'prefix': prefix}
        return self.api_client._request_with_params(POST, MERGE_FILE, self.MCS_API, params, self.token, None)

    def read_chunks(self, file, chunk_size=10485760):
        while True:
            data = file.read(chunk_size)
            if not data:
                break
            yield data

    def upload_to_bucket(self, bucket_id, file_path, prefix=''):
        if os.stat(file_path).st_size == 0:
            return 'File size cannot be 0'
        file_name = os.path.basename(file_path)
        file_size = os.stat(file_path).st_size
        with open(file_path, 'rb') as file:
            file_hash = md5(file.read()).hexdigest()
        result = self.check_file(bucket_id, file_hash, file_name, prefix)
        if not (result['data']['file_is_exist']):
            with open(file_path, 'rb') as file:
                i = 0
                queue = Queue()
                self.api_client.upload_progress_bar(file_name, file_size)
                for chunk in self.read_chunks(file):
                    i += 1
                    queue.put((str(i), chunk))
                file.close()
            threads = list()
            for i in range(3):
                worker = threading.Thread(target=self.thread_upload_chunk, args=(queue, file_hash, file_name))
                threads.append(worker)
                worker.start()
            for thread in threads:
                thread.join()
            if not (result['data']['ipfs_is_exist']):
                self.merge_file(bucket_id, file_hash, file_name, prefix)
            return 'Upload success'
        return 'File already existed'

    def upload_folder(self, bucket_id, folder_path, prefix=''):
        path = os.path.basename(folder_path)
        folder_name = os.path.splitext(path)[0]
        self.create_folder(folder_name, bucket_id, prefix)
        files = os.listdir(folder_path)
        success = []
        for f in files:
            f_path = os.path.join(folder_path, f)
            if os.path.isdir(f_path):
                success.extend(self.upload_folder(bucket_id, f_path, os.path.join(prefix, folder_name)))
            else:
                self.upload_to_bucket(bucket_id, f_path, os.path.join(prefix, folder_name))
                time.sleep(0.5)
                success.append(f_path)
        return success

    def download_file(self, bucket_id, file_name, prefix='', dir=''):
        file_list = self.get_full_file_list(bucket_id, prefix)
        for file in file_list:
            if file['Name'] == file_name:
                url = file['IpfsUrl']
                print(url)
                download_path = os.path.join(dir, file_name)
                with open(download_path, 'wb') as f:
                    data = urllib.request.urlopen(url)
                    f.write(data.read())
                return 'success'
        return 'file does not exist'
