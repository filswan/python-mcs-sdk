import os
from dotenv import load_dotenv
from mcs.upload.mcs_upload import MCSUpload

chain_name = "polygon.mumbai"

def test_auto_upload():
    load_dotenv(".env_test")
    private_key = os.getenv('private_key')
    rpc_endpoint = os.getenv('rpc_endpoint')
    api_key = os.getenv('api_key')
    access_token = os.getenv('access_token')

    filepath = "/images/log_mcs.png"
    parent_path = os.path.abspath(os.path.dirname(__file__))

    up = MCSUpload(chain_name, private_key, rpc_endpoint, api_key, access_token, parent_path+filepath)
    up.approve_token(1)
    file_data, need_pay = up.stream_upload()
    print(up.estimate_amount)

    if need_pay:
        up.pay()
        up.mint('a_image')