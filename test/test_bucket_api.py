import pytest
import os
from dotenv import load_dotenv
from swan_mcs import BucketAPI, APIClient


@pytest.mark.skip(reason="no way of currently testing this")
class TestBucketAPI:
    def login(self):
        load_dotenv(".env_test")
        api_key = os.getenv('api_key')
        access_token = os.getenv('access_token')
        chain_name = os.getenv("chain_name")
        api = BucketAPI(APIClient(api_key, access_token, chain_name))

        assert api
        return api

    def test_delete_bucket(self):
        api = self.login()
        print(api.delete_bucket('test-bucket'))

    def test_list_buckets(self):
        api = self.login()
        print(api.list_buckets())
        assert api.list_buckets() is not None

    def test_create_bucket(self):
        api = self.login()
        create = api.create_bucket('test-bucket')
        assert create is True

    def test_get_bucket(self):
        api = self.login()
        bucket = api.get_bucket('test-bucket')
        assert bucket.bucket_name == 'test-bucket'

    def test_create_folder(self):
        api = self.login()
        create = api.create_folder('test-bucket', 'folder1')

        assert create is True

    # def test_create_folder_with_same_name():
    #     api = login()
    #     create = api.create_folder('test-bucket', 'folder1')
    #     print(create)

    def test_upload_file(self):
        api = self.login()
        filepath = "/images/log_mcs.png"
        parentpath = os.path.abspath(os.path.dirname(__file__))
        file = api.upload_file('test-bucket', "folder1/swan_mcs-logo.png", parentpath + filepath)
        assert file.name == "swan_mcs-logo.png"

    def test_get_file(self):
        api = self.login()
        file = api.get_file('test-bucket', 'folder1/swan_mcs-logo.png')

        assert file.name == "swan_mcs-logo.png"

    def test_get_file_list(self):
        api = self.login()
        list = api.list_files('test-bucket', 'folder1')

        assert len(list) == 1
        assert list[0].name == 'swan_mcs-logo.png'

    def test_download_file(self):
        api = self.login()
        result = api.download_file('test-bucket', 'folder1/swan_mcs-logo.png', "aaaa.png")

        assert result is True

    def test_delete_file(self):
        api = self.login()
        delete = api.delete_file('test-bucket', 'folder1/swan_mcs-logo.png')

        assert delete is True

    def test_upload_ipfs_folder(self):
        api = self.login()
        res = api.upload_ipfs_folder('test-bucket', 'ipfs-folder', 'images')

        print(res)
