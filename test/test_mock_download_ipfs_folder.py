import io
import tarfile
from pathlib import Path

import requests_mock
import pytest
from swan_mcs.common import constants as c


class TestDownloadIpfsFolder:
    @pytest.fixture
    def mock_requests(self, shared_current_time, shared_mock_bucket, shared_bucket_list):
        self.bucket_name = "test-bucket-1"
        self.object_name = "test-object-1"
        self.folder_path = Path("test_dir") / ("test_folder" + shared_current_time)
        self.bucket_api = shared_mock_bucket
        data = b"test content123445667"
        # Mock the tarfile content
        with io.BytesIO() as file:
            with tarfile.open(fileobj=file, mode="w:gz") as tar:
                tarfile.TarInfo("test_dir/test-folder/")
                tar_info = tarfile.TarInfo("test_dir/test-folder/file1.txt")
                tar_info.size = len(data)
                tar.addfile(tar_info, io.BytesIO(data))
            file.seek(0)
            self.tarfile_content = file.read()
        with requests_mock.Mocker() as m:
            m.get(c.BUCKET_LIST, json={'data': shared_bucket_list})
            m.get(c.GET_FILE, json={"status": "success", "data": {
                'name': "test-file-name-1",
                'address': "simple_address",
                'bucket_uid': "simple_bucket_uid",
                'created_at': "2023-03-28T20:09:45Z",
                'deleted_at': None,
                'file_hash': "simple_file_hash",
                'id': 12345,
                'is_deleted': False,
                'is_folder': False,
                'object_name': 'test-object-1',
                'payload_cid': "simple_payload_cid",
                'pin_status': "Pinned",
                'prefix': "",
                'size': 244029,
                'type': 2,
                'updated_at': "2023-03-28T20:09:45Z",
            }})
            m.post("https://ipfs.io/api/v0/get?arg=simple_payload_cid&create=true", content=self.tarfile_content,
                   headers={"Content-Type": "application/x-tar"})
            yield m

    def test_download_ipfs_folder_success(self, mock_requests, tmp_path):
        result = self.bucket_api.download_ipfs_folder(self.bucket_name, self.object_name, self.folder_path)

        # Check the result
        assert result is True
        assert Path(self.folder_path).exists() is True

    def test_download_ipfs_folder_failure(self, mock_requests, tmp_path):
        assert Path(self.folder_path).exists() is False
        mock_requests.post("https://ipfs.io/api/v0/get?arg=simple_payload_cid&create=true",
                           status_code=400,
                           content=self.tarfile_content,
                           headers={"Content-Type": "application/x-tar"})
        result = self.bucket_api.download_ipfs_folder(self.bucket_name, self.object_name, self.folder_path)

        # Check the result
        assert result is False
        assert Path(self.folder_path).exists() is False


