import pytest
import os
from dotenv import load_dotenv

from upload.free_upload import FreeUpload

def test_free_upload():
    load_dotenv()
    wallet_address = os.getenv('wallet_address')
    private_key = os.getenv('private_key')
    web3_api = os.getenv('web3_api')

    file_path = "/images/log_mcs.png"
    parent_path = os.path.abspath(os.path.dirname(__file__))

    upload = FreeUpload(wallet_address, private_key, web3_api, parent_path+file_path)
    # test free upload
    result = upload.free_upload()
    assert result == 'free_upload' or result == 'payment success'
    # test free stream upload
    result = upload.stream_upload()
    assert result == 'free_stream_upload' or result == 'payment success'
