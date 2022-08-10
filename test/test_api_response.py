import pytest
import os
from mcs.api import McsAPI
from mcs.contract import ContractAPI


@pytest.fixture
def info():
    wallet_info = {
        'wallet_address': '*',
        'private_key': '*',
        'web3_api': '*',
    }
    return wallet_info


'''
@pytest.fixture
def data():
    data = {}
    # example of return responses
    data['param'] = {'status': 'success', 'data': {'GAS_LIMIT': 8000000, 'LOCK_TIME': 6, 'MINT_CONTRACT_ADDRESS': '0x1A1e5AC88C493e0608C84c60b7bb5f04D9cF50B3',
            'PAYMENT_CONTRACT_ADDRESS': '0x80a186DCD922175019913b274568ab172F6E20b1', 'PAYMENT_RECIPIENT_ADDRESS': '0xc4fcaAdCb0b00a9501e56215c37B10fAF9e79c0a',
            'PAY_MULTIPLY_FACTOR': 1.5, 'USDC_ADDRESS': '0xe11A86849d99F524cAC3E7A0Ec1241828e332C62'}}
    data['price_rate'] = {'status': 'success', 'data': 5}
    data['payment_info'] = {"status": "success", "data": {"w_cid": "64fc6e48-cad9-430d-8a4f-0821e55020c4QmcLqL4xSXzTQUfV2GMjyHoxM8eSH3WJjQjjByaVDzoGEa",
            "pay_amount": "", "pay_tx_hash": "", "token_address": ""}}
    return data

def test_mcs_api(info, data):
    wallet_address = info['wallet_address']
    payload_cid = '*'
    source_file_upload_id = '*'

    api = McsAPI()
    result = {}
    # API: https://mcs-api.filswan.com/api/v1/common/system/params
    result['param'] = api.get_params()
    # API: https://mcs-api.filswan.com/api/v1/billing/price/filecoin
    result['price_rate'] = api.get_price_rate()
    # API: https://mcs-api.filswan.com/api/v1/billing/deal/lockpayment/info?payload_cid=&wallet_address=&source_file_upload_id=
    result['payment_info'] = api.get_payment_info(payload_cid, wallet_address, source_file_upload_id)
    # API: https://mcs-api.filswan.com/api/v1/storage/tasks/deals?wallet_address=
    #result['user_tasks_deal'] = api.get_user_tasks_deals(wallet_address)
    # API: https://mcs-api.filswan.com/api/v1/storage/deal/detail/0?wallet_address=&source_file_upload_id=
    #result['deal_detail'] = api.get_deal_detail(wallet_address, source_file_upload_id)
    assert result == data
'''


def test_approve_usdc(info):
    wallet_address = info['wallet_address']
    private_key = info['private_key']
    web3_api = info['web3_api']

    w3_api = ContractAPI(web3_api)
    w3_api.approve_usdc(wallet_address,
                        private_key, "1")


def test_upload_file_pay(info):
    wallet_address = info['wallet_address']
    private_key = info['private_key']
    web3_api = info['web3_api']

    w3_api = ContractAPI(web3_api)
    api = McsAPI()

    # upload file to mcs
    filepath = "/images/log_mcs.png"
    father_path = os.path.abspath(os.path.dirname(__file__))
    upload_file = api.upload_file(wallet_address, father_path + filepath)
    # test upload file
    assert upload_file['status'] == 'success'
    file_data = upload_file["data"]
    payload_cid, source_file_upload_id, nft_uri, file_size, w_cid = file_data['payload_cid'], file_data[
        'source_file_upload_id'], file_data['ipfs_url'], file_data['file_size'], file_data['w_cid']
    # get the global variable
    params = api.get_params()["data"]
    # test get params api
    assert api.get_params()['status'] == 'success'
    # get filcoin price
    rate = api.get_price_rate()["data"]
    # test get price rate api
    assert api.get_price_rate()['status'] == 'success'
    # test upload_file_pay contract
    w3_api.upload_file_pay(wallet_address, private_key, file_size, w_cid, rate, params)
    # test get payment info api
    payment_info = api.get_payment_info(payload_cid, wallet_address, source_file_upload_id)
    assert payment_info['status'] == 'success'
    assert payment_info['data']['w_cid'] == w_cid
    # test get deal detail
    deal_detail = api.get_deal_detail(wallet_address, source_file_upload_id)
    assert deal_detail['status'] == 'success'
    assert deal_detail['data'] != None


def test_mint_nft(info):
    wallet_address = info['wallet_address']
    private_key = info['private_key']
    web3_api = info['web3_api']

    w3_api = ContractAPI(web3_api)
    api = McsAPI()

    # upload file to mcs
    filepath = "/images/log_mcs.png"
    filename = "log_mcs.png"
    father_path = os.path.abspath(os.path.dirname(__file__))
    upload_file = api.upload_file(wallet_address, father_path + filepath)
    # test upload file
    assert upload_file['status'] == 'success'
    file_data = upload_file["data"]
    payload_cid, source_file_upload_id, nft_uri, file_size, w_cid = file_data['payload_cid'], file_data[
        'source_file_upload_id'], file_data['ipfs_url'], file_data['file_size'], file_data['w_cid']
    # get the global variable
    params = api.get_params()["data"]
    # test get params api
    assert api.get_params()['status'] == 'success'
    # get filcoin price
    rate = api.get_price_rate()["data"]
    # test get price rate api
    assert api.get_price_rate()['status'] == 'success'
    # test upload_file_pay contract
    tx_hash = w3_api.upload_file_pay(wallet_address, private_key, file_size, w_cid, rate, params)
    print(tx_hash)
    # upload nft metadata
    nft_metadata = api.upload_nft_metadata(wallet_address, filename, nft_uri, tx_hash, file_size)
    # test upload nft metadata
    assert nft_metadata['status'] == 'success'
    meta_url = nft_metadata['data']['ipfs_url']
    print(meta_url)
    # test mint nft contract
    tx_hash, token_id = w3_api.mint_nft(wallet_address,
                                        private_key, meta_url)
    print(tx_hash)

    # update mint info
    mint_address = params['MINT_CONTRACT_ADDRESS']
    mint_info = api.get_mint_info(source_file_upload_id, None, tx_hash, token_id, mint_address)
    # test update mint info
    assert mint_info['status'] == 'success'
    assert mint_info['data']['source_file_upload_id'] == source_file_upload_id
    assert mint_info['data']['nft_tx_hash'] == tx_hash
    assert mint_info['data']['token_id'] == str(token_id)
    assert mint_info['data']['mint_address'] == mint_address
