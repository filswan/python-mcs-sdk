import pytest
import os, time
from mcs.contract import ContractAPI
from mcs.api import McsAPI

wallet_address = "*"
private_key = "*"
web3_api = "*"


def test_approve_usdc():
    w3_api = ContractAPI(web3_api)
    w3_api.approve_usdc(wallet_address,
                        private_key, "1")


def test_upload_file_pay():
    w3_api = ContractAPI(web3_api)
    api = McsAPI()
    # upload file to mcs
    filepath = "/images/log_mcs.png"
    father_path = os.path.abspath(os.path.dirname(__file__))
    upload_file = api.upload_file(wallet_address, father_path + filepath)
    file_data = upload_file["data"]
    payload_cid, source_file_upload_id, nft_uri, file_size, w_cid = file_data['payload_cid'], file_data[
        'source_file_upload_id'], file_data['ipfs_url'], file_data['file_size'], file_data['w_cid']
    # get the global variable
    params = api.get_params()["data"]
    # get filcoin price
    rate = api.get_price_rate()["data"]
    # test upload_file_pay contract
    w3_api.upload_file_pay(wallet_address, private_key, file_size, w_cid, rate, params)

def test_stream_upload_file_pay():
    w3_api = ContractAPI(web3_api)
    api = McsAPI()
    # upload file to mcs
    filepath = "/images/log_mcs.png"
    father_path = os.path.abspath(os.path.dirname(__file__))
    upload_file = api.stream_upload_file(wallet_address, father_path + filepath)
    file_data = upload_file["data"]
    payload_cid, source_file_upload_id, nft_uri, file_size, w_cid = file_data['payload_cid'], file_data[
        'source_file_upload_id'], file_data['ipfs_url'], file_data['file_size'], file_data['w_cid']
    # get the global variable
    params = api.get_params()["data"]
    # get filcoin price
    rate = api.get_price_rate()["data"]
    # test upload_file_pay contract
    w3_api.upload_file_pay(wallet_address, private_key, file_size, w_cid, rate, params)

def test_mint_nft():
    w3_api = ContractAPI(web3_api)
    api = McsAPI()

    # upload file to mcs
    filepath = "/images/log_mcs.png"
    filename = "log_mcs.png"
    father_path = os.path.abspath(os.path.dirname(__file__))
    upload_file = api.upload_file(wallet_address, father_path + filepath)
    file_data = upload_file["data"]
    payload_cid, source_file_upload_id, nft_uri, file_size, w_cid = file_data['payload_cid'], file_data[
        'source_file_upload_id'], file_data['ipfs_url'], file_data['file_size'], file_data['w_cid']
    # get the global variable
    params = api.get_params()["data"]
    # get filcoin price
    rate = api.get_price_rate()["data"]
    # test upload_file_pay contract
    tx_hash = w3_api.upload_file_pay(wallet_address, private_key, file_size, w_cid, rate, params)
    print(tx_hash)
    # upload nft metadata
    meta_url = api.upload_nft_metadata(wallet_address, filename, nft_uri, tx_hash, file_size)['data']['ipfs_url']
    print(meta_url)
    # test mint nft contract
    tx_hash, token_id = w3_api.mint_nft(wallet_address,
                                        private_key, meta_url)
    print(tx_hash)
    # get data_cid ,need wait some time
    # time.sleep(60)
    # data_cid = api.get_deal_detail(wallet_address, source_file_upload_id)['data']['source_file_upload_deal'][
    #     'car_file_payload_cid']
    #
    # print(data_cid)

    # update mint info
    api.get_mint_info(source_file_upload_id, None, tx_hash, token_id, wallet_address)
