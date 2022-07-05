import pytest
import os
from mcs.contract import ContractAPI
from mcs.api import McsAPI

wallet_address = "*"
private_key = "*"
web3_api = "*"


@pytest.mark.asyncio
async def test_approve_usdc():
    w3_api = ContractAPI(web3_api)
    w3_api.approve_usdc(wallet_address,
                        private_key, "1")


@pytest.mark.asyncio
async def test_upload_file_pay():
    w3_api = ContractAPI(web3_api)
    api = McsAPI()
    # upload file to mcs
    filepath = "/images/log_mcs.png"
    father_path = os.path.abspath(os.path.dirname(__file__))
    upload_file = api.upload_file(wallet_address, father_path + filepath)
    file_data = upload_file["data"]
    payload_cid, source_file_upload_id, nft_uri, file_size, w_cid = file_data['payload_cid'], file_data[
        'source_file_upload_id'], file_data['ipfs_url'], file_data['file_size'], file_data['w_cid']
    print(payload_cid, source_file_upload_id, nft_uri, file_size)

    # get the global variable
    params = api.get_params()["data"]
    # get filcoin price
    rate = api.get_price_rate()["data"]
    # test upload_file_pay contract
    w3_api.upload_file_pay(wallet_address, private_key, file_size, w_cid, rate, params)

