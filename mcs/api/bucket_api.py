from aiohttp import request
from mcs.api_client import APIClient
from mcs.common.constants import *
from hashlib import md5
from queue import Queue
import os, threading
import urllib.request
import logging

from mcs.common.utils import object_to_filename
from mcs.object.bucket_storage import Bucket, File


class BucketAPI(object):
    def __init__(self, api_client=None):
        '''Initialize Bucket API

        Parameter:
            :type api_client: obj APIClient
            :param api_client: The mcs api client object
        '''
        if api_client is None:
            api_client = APIClient()
        self.api_client = api_client
        self.MCS_API = api_client.MCS_API
        self.token = self.api_client.token

    def list_buckets(self):
        '''Retrieve bucket list

        Return: 
            :type bucket_info_list: list[] Bucket
            :return bucket_info_list: A list of all buckets created on multichain.storage
        '''
        try:
            result = self.api_client._request_without_params(GET, BUCKET_LIST, self.MCS_API, self.token)
            bucket_info_list = []
            data = result['data']
            for bucket in data:
                bucket_info: Bucket = Bucket(bucket)
                bucket_info_list.append(bucket_info)
            return bucket_info_list
        except:
            logging.error("\033[31m" + result['message'] + "\033[0m")
            return
        

    def create_bucket(self, bucket_name):
        '''Create bucket on multichain.storage

        Parameters:
            :type bucket_name: str
            :param bucket_name: Name of the new bucket

        Return:
            :type: bool
            :return: True/False as creation result
        '''
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
        '''Delete bucket from multichain.storage

        Parameters:
            :type bucket_name: str
            :param bucket_name: Name of the bucket to delete

        Return:
            :type: bool
            :return: True/False as creation result
        '''
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
        '''Get bucket information
        
        Parameters:
            :type bucket_name: str
            :param bucket_name: Name of the bucket for searching

            :type bucket_id: str
            :param bucket_id: Bucket uuid for searching

        Return:
            :type bucket: obj Bucket
            :return bucket: A bucket object retrieved
        '''
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
        '''Retrieve file object

        Parameters:
        :type bucket_name: str
        :param bucket_name: Name of target bucket

        :type object_name: str
        :type object_name: Path and name of the target file

        Return:
        :type file: obj File
        :return file: File object
        '''
        try:
            prefix, file_name = object_to_filename(object_name)
            file_list = self._get_full_file_list(bucket_name, prefix)
            
            for file in file_list:
                if file.name == file_name:
                    return file
            logging.error("\033[31mCan't find this object\033[0m")
            return None
        except:
            logging.error("\033[31mCan't find this bucket\033[0m")
            return

    def create_folder(self, bucket_name, folder_name, prefix=''):
        '''Create folder within bucket

        Parameters:
            :type bucket_name: str
            :param bucket_name: Target bucket for folder creation

            :type folder_name: str
            :param folder_name: New folder name

            :type prefix: str
            :param prefix: Target path within bucket for folder creation

        Return:
            :type: bool
            :return: True/False for 
        '''
        try:
            bucket_id = self._get_bucket_id(bucket_name)
            params = {"file_name": folder_name, "prefix": prefix, "bucket_uid": bucket_id}
            result = self.api_client._request_with_params(POST, CREATE_FOLDER, self.MCS_API, params, self.token, None)
            if result['status'] == 'success':
                logging.info("\033[31mFolder created successfully\033[0m")
                return True
            else:
                logging.error("\033[31m" + result['message']+ "\033[0m")
                return False
        except:
            logging.error("\033[31mCan't create this folder")
            return 

    def delete_file(self, bucket_name, object_name):
        '''Delete file from bucket

        Parameters:
            :type bucket_name: str
            :param bucket_name: Bucket name for target file

            :type object_name: str
            :param object_name: Path and file name for the target file

        Return:
            :type: bool
            :return: True/False as deletion result
        '''
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
        '''Get file list from a bucket

        Parameters:
            :type bucket_name: str
            :param bucket_name: Target bucket name

            :type prefix: str
            :param prefix: Target path within the bucket for file list retrieve

            :type limit: str
            :param limit: Number of file per page

            :type offset: str
            :param limit: Number of page

        Return:
            :type file_list: list[] File
            :return file_list: List of file object from the target bucket
        '''
        bucket_id = self._get_bucket_id(bucket_name)
        params = {'bucket_uid': bucket_id, 'prefix': prefix, 'limit': limit, 'offset': offset}
        result = self.api_client._request_with_params(GET, FILE_LIST, self.MCS_API, params, self.token, None)
        if result['status'] == 'success':
            files = result['data']['file_list']
            file_list = []
            for file in files:
                file_info: File = File(file)
                file_list.append(file_info)
            return file_list
        else:
            logging.error("\033[31m" + result['message'] + "\033[0m")
            return False


    def upload_file(self, bucket_name, object_name, file_path):
        '''Upload file to bucket

        Parameters:
            :type bucket_name: str
            :param bucket_name: Target bucket name

            :type object_name: str
            :param object_name: Remote file path and name within bucket

            :type file_path: str
            :param file_path: Local file path

        Return:
            :type file_info: obj File
            :return: File object for successfully uploaded file
        '''
        prefix, file_name = object_to_filename(object_name)
        bucket_id = self._get_bucket_id(bucket_name)
        if os.stat(file_path).st_size == 0:
            logging.error("\033[31mFile size cannot be 0\033[0m")
            return None
        file_size = os.stat(file_path).st_size
        with open(file_path, 'rb') as file:
            file_hash = md5(file.read()).hexdigest()
        result = self._check_file(bucket_id, file_hash, file_name, prefix)
        if result is None:
            logging.error("\033[31mCan't find this bucket\033[0m")
            return
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
            logging.info("\033[32mFile upload successfully\033[0m")
            return file_info
        logging.error("\033[31mFile already exists\033[0m")
        return None

    def _upload_to_bucket(self, bucket_name, file_path, prefix=''):
        if os.path.isdir(file_path):
            return self.upload_folder(bucket_name, file_path, prefix)
        else:
            file_name = os.path.basename(file_path)
            return self.upload_file(bucket_name, os.path.join(prefix,file_name), file_path)

    def upload_folder(self, bucket_name, folder_path, prefix=''):
        '''Upload folder to bucket

        Parameter:
            :type bucket_name: str
            :param bucket_name: Target bucket name

            :type folder_path: str
            :param folder_path: Local folder path

            :type prefix: str
            :param prefix: Remote folder path

        Return:
            :type res: list[] File
            :return res: list of uploaded file in the folder
        '''
        folder_name = os.path.basename(folder_path)
        self.create_folder(bucket_name, folder_name, prefix)
        res = []
        files = os.listdir(folder_path)
        for f in files:
            f_path = os.path.join(folder_path, f)
            upload = self._upload_to_bucket(bucket_name, f_path, os.path.join(prefix, folder_name))
            res.append(upload)
        
        return res


    def download_file(self, bucket_name, object_name, local_filename):
        '''Download file from bucket

        Parameters:
            :type bucket_name: str
            :param bucket_name: Target bucket name

            :type object_name: str
            :param object_name: Remote file path and file name

            :type local_filename: str
            :param local_filename: Path and name for store file locally

        Return
            :type: bool
            :return: True/False status of download
        '''
        file = self.get_file(bucket_name, object_name)
        if file is not None:
            ipfs_url = file.ipfs_url
            with open(local_filename, 'wb') as f:
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
                file_info: File = File(file)
                file_list.append(file_info)
        return file_list

    def _get_file_info(self, file_id):
        params = {'file_id': file_id}
        result = self.api_client._request_with_params(GET, FILE_INFO, self.MCS_API, params, self.token, None)
        file_info = File(result['data'])
        return file_info
