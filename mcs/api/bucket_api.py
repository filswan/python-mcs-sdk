from aiohttp import request
from mcs.api_client import APIClient
from mcs.common.constants import *
from hashlib import md5
from queue import Queue
import os, threading
import urllib.request
import logging
import glob
import shutil

from mcs.common.utils import object_to_filename
from mcs.object.bucket_storage import Bucket, File


class BucketAPI(object):
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = APIClient()
        self.api_client = api_client
        self.MCS_API = api_client.MCS_API
        self.token = self.api_client.token
        self.gateway = self.get_gateway()

    def list_buckets(self):
        try:
            result = self.api_client._request_without_params(GET, BUCKET_LIST, self.MCS_API, self.token)
            bucket_info_list = []
            data = result['data']
            for bucket in data:
                bucket_info: Bucket = Bucket(bucket)
                bucket_info_list.append(bucket_info)
            return bucket_info_list
        except:
            logging.error("\033[31m" + 'error' + "\033[0m")
            return

    def create_bucket(self, bucket_name):
        params = {'bucket_name': bucket_name}
        try:
            result = self.api_client._request_with_params(POST, CREATE_BUCKET, self.MCS_API, params, self.token, None)
            if result['status'] == 'success':
                logging.info("\033[32mBucket created successfully\033[0m")
                return True
            else:
                logging.error("\033[31m" + result['message'] + "\033[0m")
        except:
            logging.error("\033[31mThis bucket already exists\033[0m")

        return False

    def delete_bucket(self, bucket_name):
        try:
            bucket_id = self._get_bucket_id(bucket_name)
            params = {'bucket_uid': bucket_id}
            result = self.api_client._request_with_params(GET, DELETE_BUCKET, self.MCS_API, params, self.token, None)
            if result['status'] == 'success':
                logging.info("\033[32mBucket delete successfully\033[0m")
                return True
        except:
            if result is None:
                logging.error("\033[31mCan't find this bucket\033[0m")
        return False

    def get_bucket(self, bucket_name='', bucket_id=''):
        bucketlist = self.list_buckets()
        if bucket_id != '' and bucket_name != '':
            for bucket in bucketlist:
                if bucket.bucket_name == bucket_name and bucket.bucket_uid == bucket_id:
                    return bucket
        if bucket_name != '' and bucket_id == '':
            for bucket in bucketlist:
                if bucket.bucket_name == bucket_name:
                    return bucket
        if bucket_name == '' and bucket_id != '':
            for bucket in bucketlist:
                if bucket.bucket_uid == bucket_id:
                    return bucket
        logging.error("\033[31mUser does not have this bucket\033[0m")
        return None

    # object name
    def get_file(self, bucket_name, object_name):
        try:
            bucket_id = self._get_bucket_id(bucket_name)
            params = {"bucket_uid": bucket_id, "object_name": object_name}

            result = self.api_client._request_with_params(GET, GET_FILE, self.MCS_API, params, self.token, None)

            if result:
                return File(result['data'], self.gateway)
        except:
            print('error')
        return

    def create_folder(self, bucket_name, folder_name, prefix=''):
        try:
            bucket_id = self._get_bucket_id(bucket_name)
            params = {"file_name": folder_name, "prefix": prefix, "bucket_uid": bucket_id}
            result = self.api_client._request_with_params(POST, CREATE_FOLDER, self.MCS_API, params, self.token, None)
            if result['status'] == 'success':
                logging.info("\033[31mFolder created successfully\033[0m")
                return True
            else:
                logging.error("\033[31m" + result['message'] + "\033[0m")
                return False
        except:
            logging.error("\033[31mCan't create this folder")
            return

    def delete_file(self, bucket_name, object_name):
        try:
            prefix, file_name = object_to_filename(object_name)
            file_list = self._get_full_file_list(bucket_name, prefix)

            file_id = ''
            for file in file_list:
                if file.name == file_name:
                    file_id = file.id
            params = {'file_id': file_id}
            if file_id == '':
                logging.error("\033[31mCan't find the file\033[0m")
                return False
            result = self.api_client._request_with_params(GET, DELETE_FILE, self.MCS_API, params, self.token, None)
            if result['status'] == 'success':
                logging.info("\033[32mFile delete successfully\033[0m")
                return True
            else:
                logging.error("\033[31mCan't delete the file\033[0m")
                return False
        except:
            logging.error("\033[31mCan't find this bucket\033[0m")
            return

    def list_files(self, bucket_name, prefix='', limit='10', offset="0"):
        bucket_id = self._get_bucket_id(bucket_name)
        params = {'bucket_uid': bucket_id, 'prefix': prefix, 'limit': limit, 'offset': offset}
        result = self.api_client._request_with_params(GET, FILE_LIST, self.MCS_API, params, self.token, None)
        if result['status'] == 'success':
            files = result['data']['file_list']
            file_list = []
            for file in files:
                file_info: File = File(file, self.gateway)
                file_list.append(file_info)
            return file_list
        else:
            logging.error("\033[31m" + result['message'] + "\033[0m")
            return False

    def upload_file(self, bucket_name, object_name, file_path, replace=False):
        prefix, file_name = object_to_filename(object_name)
        bucket_id = self._get_bucket_id(bucket_name)

        # if os.stat(file_path).st_size == 0:
        #     logging.error("\033[31mFile size cannot be 0\033[0m")
        #     return None

        file_size = os.stat(file_path).st_size
        with open(file_path, 'rb') as file:
            file_hash = md5(file.read()).hexdigest()
        result = self._check_file(bucket_id, file_hash, file_name, prefix)
        if result is None:
            logging.error("\033[31mCan't find this bucket\033[0m")
            return
        # Replace file if already existed
        if result['data']['file_is_exist'] and replace:
            self.delete_file(bucket_name, object_name)
            result = self._check_file(bucket_id, file_hash, file_name, prefix)
        if not (result['data']['file_is_exist']):
            if not (result['data']['ipfs_is_exist']):
                with open(file_path, 'rb') as file:
                    i = 0
                    queue = Queue()
                    self.api_client.upload_progress_bar(file_name, file_size)
                    for chunk in self._read_chunks(file):
                        i += 1
                        queue.put((str(i), chunk))
                    file.close()
                threads = list()
                for i in range(3):
                    worker = threading.Thread(target=self._thread_upload_chunk, args=(queue, file_hash, file_name))
                    threads.append(worker)
                    worker.start()
                for thread in threads:
                    thread.join()
                result = self._merge_file(bucket_id, file_hash, file_name, prefix)
            file_id = result['data']['file_id']
            file_info = self._get_file_info(file_id)
            self._create_folders(bucket_name, prefix)
            logging.info("\033[32mFile upload successfully\033[0m")
            return file_info
        logging.error("\033[31mFile already exists\033[0m")
        return None
    
    def _create_folders(self, bucket_name, path):
        bucket_id = self._get_bucket_id(bucket_name)
        path, folder_name = object_to_filename(path)
        while folder_name:
            params = {"file_name": folder_name, "prefix": path, "bucket_uid": bucket_id}
            self.api_client._request_with_params(POST, CREATE_FOLDER, self.MCS_API, params, self.token, None)
            path, folder_name = object_to_filename(path)

    def _upload_to_bucket(self, bucket_name, file_path, prefix=''):
        if os.path.isdir(file_path):
            return self.upload_folder(bucket_name, file_path, prefix)
        else:
            file_name = os.path.basename(file_path)
            return self.upload_file(bucket_name, os.path.join(prefix, file_name), file_path)

    def upload_folder(self, bucket_name, folder_path, prefix=''):
        folder_name = os.path.basename(folder_path)
        self.create_folder(bucket_name, folder_name, prefix)
        res = []
        files = os.listdir(folder_path)
        for f in files:
            f_path = os.path.join(folder_path, f)
            upload = self._upload_to_bucket(bucket_name, f_path, os.path.join(prefix, folder_name))
            res.append(upload)

        return res

    # def upload_ipfs_folder(self, bucket_name, object_name, folder_path):
    #     folder_name = os.path.basename(object_name) or os.path.basename(folder_path)
    #     prefix = os.path.normpath(os.path.dirname(object_name)) if os.path.dirname(object_name) else ''
    #     bucket_uid = self._get_bucket_id(bucket_name)
    #     files = self._read_files(folder_path, folder_name)
    #     form_data = {"folder_name": folder_name, "prefix": prefix, "bucket_uid": bucket_uid}
    #     res = self.api_client._request_with_params(POST, PIN_IPFS, self.MCS_API, form_data, self.token, files)
    #     if res:
    #         folder = (File(res["data"], self.gateway))
    #         return folder
    #     else:
    #         logging.error("\033[31mIPFS Folder Upload Error\033[0m")

    def download_file(self, bucket_name, object_name, local_filename):
        file = self.get_file(bucket_name, object_name)
        if file is not None:
            ipfs_url = file.ipfs_url
            with open(local_filename, 'wb') as f:
                if file.size > 0:
                    data = urllib.request.urlopen(ipfs_url)
                    f.write(data.read())
            logging.info("\033[32mFile download successfully\033[0m")
            return True
        logging.error('\033[31mFile does not exist\033[0m')
        return False

    def _check_file(self, bucket_id, file_hash, file_name, prefix=''):
        params = {'bucket_uid': bucket_id, 'file_hash': file_hash, 'file_name': file_name, 'prefix': prefix}
        return self.api_client._request_with_params(POST, CHECK_UPLOAD, self.MCS_API, params, self.token, None)

    def _upload_chunk(self, file_hash, file_name, chunk):
        params = {'hash': file_hash, 'file': (file_name, chunk)}
        return self.api_client._request_bucket_upload(UPLOAD_CHUNK, self.MCS_API, params, self.token)

    def _thread_upload_chunk(self, queue, file_hash, file_name):
        while not queue.empty():
            chunk = queue.get()
            self._upload_chunk(file_hash, chunk[0] + '_' + file_name, chunk[1])

    def _merge_file(self, bucket_id, file_hash, file_name, prefix=''):
        params = {'bucket_uid': bucket_id, 'file_hash': file_hash, 'file_name': file_name, 'prefix': prefix}
        return self.api_client._request_with_params(POST, MERGE_FILE, self.MCS_API, params, self.token, None)

    def _read_chunks(self, file, chunk_size=10485760):
        while True:
            data = file.read(chunk_size)
            if not data:
                break
            yield data

    def _get_bucket_id(self, bucket_name):
        bucketlist = self.list_buckets()
        for bucket in bucketlist:
            if bucket.bucket_name == str(bucket_name):
                return bucket.bucket_uid
        return None

    def _get_full_file_list(self, bucket_name, prefix=''):
        bucket_id = self._get_bucket_id(bucket_name)
        params = {'bucket_uid': bucket_id, 'prefix': prefix, 'limit': 10, 'offset': 0}
        count = self.api_client._request_with_params(GET, FILE_LIST, self.MCS_API, params, self.token, None)['data'][
            'count']
        file_list = []
        for i in range(count // 10 + 1):
            params['offset'] = i * 10
            result = \
                self.api_client._request_with_params(GET, FILE_LIST, self.MCS_API, params, self.token, None)['data'][
                    'file_list']
            for file in result:
                file_info: File = File(file, self.gateway)
                file_list.append(file_info)
        return file_list

    def _get_file_info(self, file_id):
        params = {'file_id': file_id}
        result = self.api_client._request_with_params(GET, FILE_INFO, self.MCS_API, params, self.token, None)
        file_info = File(result['data'], self.gateway)
        return file_info

    def get_gateway(self):
        result = self.api_client._request_without_params(GET, GET_GATEWAY, self.MCS_API, self.token)
        return 'https://' + result['data'][0]

    def _read_files(self, root_folder, folder_name):
        # Create an empty list to store the file tuples
        file_dict = []

        # Use glob to retrieve the file paths in the directory and its subdirectories
        file_paths = glob.glob(os.path.join(root_folder, '**', '*'), recursive=True)

        # Loop through each file path and read the contents of the file
        for file_path in file_paths:
            if os.path.isfile(file_path):
                # Get the relative path from the root folder
                upload_path = folder_name + "/" + os.path.relpath(file_path, root_folder)
                file_dict.append(('files', (
                    upload_path, open(file_path, 'rb'))))

        return file_dict
