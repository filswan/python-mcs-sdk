import os
from dotenv import load_dotenv
from mcs.upload.mcs_upload import MCSUpload

def test_auto_upload():
    load_dotenv(".env_main")
    wallet_address = os.getenv('wallet_address')
    private_key = os.getenv('private_key')
    rpc_endpoint = os.getenv('rpc_endpoint')

    filepath = "/images/log_mcs.png"
    parent_path = os.path.abspath(os.path.dirname(__file__))

    up = MCSUpload("polygon.mainnet", wallet_address, private_key, rpc_endpoint, parent_path+filepath)
    up.approve_token(1)
    file_data, need_pay = up.stream_upload()
    print(up.estimate_amount)

    if need_pay:
        up.pay()
        up.mint('a_image')