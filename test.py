import os
from dotenv import load_dotenv

from upload.free_upload import FreeUpload

def test_free_upload():
    load_dotenv()
    wallet_address = os.getenv('wallet_address')
    private_key = os.getenv('private_key')
    web3_api = os.getenv('web3_api')

    file_path = "/test/images/log_mcs.png"
    parent_path = os.path.abspath(os.path.dirname(__file__))

    upload = FreeUpload(wallet_address, private_key, web3_api, parent_path+file_path)
    data = upload.upload()
    p = upload.pay()
    print(data)

if __name__ == "__main__":
    test_free_upload()
