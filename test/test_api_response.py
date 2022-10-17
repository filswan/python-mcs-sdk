import os

import web3
from web3 import Web3
from dotenv import load_dotenv
from mcs.api import McsAPI
from mcs.common.params import Params
from mcs.contract import ContractAPI
from mcs.common.utils import get_amount

chain_name = "main"


def test_info():
    load_dotenv(".env_" + chain_name)
    wallet_info = {
        'wallet_address': os.getenv('wallet_address'),
        'private_key': os.getenv('private_key'),
        'rpc_endpoint': os.getenv('rpc_endpoint'),
    }
    return wallet_info


def test_approve_usdc():
    info = test_info()
    wallet_address = info['wallet_address']
    private_key = info['private_key']
    rpc_endpoint = info['rpc_endpoint']
    w3_api = ContractAPI(rpc_endpoint, chain_name)
    w3_api.approve_usdc(wallet_address, private_key, 1)


def test_upload_file_pay():
    info = test_info()
    wallet_address = info['wallet_address']
    private_key = info['private_key']
    rpc_endpoint = info['rpc_endpoint']

    w3_api = ContractAPI(rpc_endpoint, chain_name)
    api = McsAPI(Params(chain_name).MCS_API)
    api.get_jwt_token(wallet_address,private_key, "polygon.mainnet")
    # upload file to mcs
    filepath = "/images/log_mcs.png"
    parent_path = os.path.abspath(os.path.dirname(__file__))
    upload_file = api.upload_file(wallet_address, parent_path + filepath)
    print(upload_file)
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
    amount = get_amount(file_size, rate)
    approve_amount = int(web3.Web3.toWei(amount, 'ether') * float(params['pay_multiply_factor']))
    w3_api.approve_usdc(wallet_address, private_key, approve_amount)
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


def test_mint_nft():
    info = test_info()
    wallet_address = info['wallet_address']
    private_key = info['private_key']
    rpc_endpoint = info['rpc_endpoint']

    w3_api = ContractAPI(rpc_endpoint, chain_name)
    api = McsAPI(Params(chain_name).MCS_API)
    api.get_jwt_token(wallet_address,private_key, "polygon.mainnet")
    w3 = Web3(Web3.HTTPProvider(rpc_endpoint))

    # upload file to mcs
    filepath = "/images/log_mcs.png"
    filename = "log_mcs.png"
    parent_path = os.path.abspath(os.path.dirname(__file__))
    upload_file = api.upload_file(wallet_address, parent_path + filepath)
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
    amount = get_amount(file_size, rate)
    approve_amount = int(w3.toWei(amount, 'ether') * float(params['pay_multiply_factor']))
    w3_api.approve_usdc(wallet_address, private_key, approve_amount)
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
    mint_address = params['mint_contract_address']
    mint_info = api.get_mint_info(source_file_upload_id, None, tx_hash, token_id, mint_address)
    # test update mint info
    assert mint_info['status'] == 'success'
    assert mint_info['data']['source_file_upload_id'] == source_file_upload_id
    assert mint_info['data']['nft_tx_hash'] == tx_hash
    assert mint_info['data']['token_id'] == int(token_id)
    assert mint_info['data']['mint_address'] == mint_address
