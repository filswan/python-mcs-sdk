from mcs.api_client import APIClient
from mcs.common.constants import *
from mcs.common.utils import get_contract_abi, get_amount
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.logs import DISCARD
from eth_account import Account
import json
import logging

from mcs.object.onchain_storage import *


class OnchainAPI(object):
    def __init__(self, api_client=None, private_key=None, rpc_url='https://polygon-rpc.com/'):
        if private_key is None:
            logging.error("Please provide private_key to use MCS Onchain Storage.")
        if api_client is None:
            api_client = APIClient()
        self.api_client = api_client
        self.MCS_API = api_client.MCS_API
        self.token = self.api_client.token
        
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.account = Account.from_key(private_key)
        if self._map_chain_name(api_client.chain_name) != self.w3.eth.chain_id:
            logging.error(f"\033[31mRPC Chain ID ({self.w3.eth.chain_id}) does not match SDK chain name ({api_client.chain_name})\033[0m")
        
        self.params = api_client.get_params()["data"]
        self.token_contract = self.w3.eth.contract(self.params['usdc_address'], abi=get_contract_abi(USDC_ABI))
        self.payment_contract = self.w3.eth.contract(self.params['payment_contract_address'], abi=get_contract_abi(SWAN_PAYMENT_ABI))
        self.mint_contract = self.w3.eth.contract(self.params['nft_collection_factory_address'], abi=get_contract_abi(MINT_ABI))


    def upload(self, file_path, pay=False, params={}):
        params['duration'] = '525'
        params['storage_copy'] = '5'
        params['file'] = (file_path, open(file_path, 'rb'))
        upload = self.api_client._request_stream_upload(UPLOAD_FILE, self.MCS_API, params, self.token)
        data = upload["data"]
        return Upload(data)


    def pay(self, source_file_upload_id, file_size, amount=''):
        payment_info = self.get_payment_info(source_file_upload_id)

        if not amount:
           amount = get_amount(float(file_size), self.params["filecoin_price"])

        decimals = self.token_contract.functions.decimals().call()
        contract_amount = int(amount * (10 ** decimals))

        hash = self._approve_usdc(int(contract_amount * float(self.params['pay_multiply_factor'])))
        print(hash)

        receipt = ''

        while not receipt:
            receipt = self.w3.eth.get_transaction_receipt(hash)

        nonce = self.w3.eth.getTransactionCount(self.account.address)
        decimals = self.token_contract.functions.decimals().call()
        lock_obj = {
            'id': payment_info.w_cid,
            'minPayment': contract_amount,
            'amount': int(contract_amount * float(self.params['pay_multiply_factor'])),
            'lockTime': 86400 * self.params['lock_time'],
            'recipient': self.params['payment_recipient_address'],
            'size': file_size,
            'copyLimit': 5,
        }

        tx = self.payment_contract.functions.lockTokenPayment(lock_obj).buildTransaction({
            'from': self.account.address,
            'nonce': nonce
        })
        signed_tx = self.w3.eth.account.signTransaction(tx, self.account._private_key)
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=CONTRACT_TIME_OUT)

        return self.w3.toHex(tx_hash)

    def mint(self, source_file_upload_id, nft, collection_address = '', quantity = 1):
        if not collection_address:
            collection_address = self.params["default_nft_collection_address"]
        metadata = self._upload_nft_metadata(nft)
        # print(metadata)

        nonce = self.w3.eth.getTransactionCount(self.account.address)
        option_obj = {
            'from': self.account.address,
            'nonce': nonce
        }
        tx = self.mint_contract.functions.mint(collection_address, self.account.address, quantity, str(metadata["data"]["ipfs_url"])).buildTransaction(option_obj)
        signed_tx = self.w3.eth.account.signTransaction(tx, self.account._private_key)
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=CONTRACT_TIME_OUT)
        result = self.mint_contract.events.TransferSingle().processReceipt(receipt, errors=DISCARD)
        id = result[0]['args']['id']
        token_id = int(id)

        self._post_mint_info(source_file_upload_id, self.w3.toHex(tx_hash), token_id, self.mint_contract.address)

        return self.w3.toHex(tx_hash), token_id

    def create_collection(self, collection_metadata):
        metadata = self._upload_nft_metadata(collection_metadata)
        # print(metadata)

        nonce = self.w3.eth.getTransactionCount(self.account.address)
        option_obj = {
            'from': self.account.address,
            'nonce': nonce
        }
        tx = self.mint_contract.functions.createCollection(str(metadata["data"]["ipfs_url"])).buildTransaction(option_obj)
        signed_tx = self.w3.eth.account.signTransaction(tx, self.account._private_key)
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=CONTRACT_TIME_OUT)
        result = self.mint_contract.events.CreateCollection().processReceipt(receipt, errors=DISCARD)
        collection_address = result[0]['args']['collectionAddress']

        return self.w3.toHex(tx_hash), collection_address

    def get_payment_info(self, source_file_upload_id):
        params = {}
        if source_file_upload_id:
            params['source_file_upload_id'] = source_file_upload_id
        payment_data = self.api_client._request_with_params(GET, PAYMENT_INFO, self.MCS_API, params, self.token, None)
        if not payment_data:
            logging.error(f"\033[31mpayment info for id {source_file_upload_id} not found \033[0m")
            return
        return Payment(payment_data["data"])

    def get_user_tasks_deals(self, page_number=None, page_size=None, file_name=None, status=None):
        params = {}
        if page_number:
            params['page_number'] = page_number
        if page_size:
            params['page_size'] = page_size
        if file_name:
            params['file_name'] = file_name
        if status:
            params['status'] = status
        return self.api_client._request_with_params(GET, TASKS_DEALS, self.MCS_API, params, self.token, None)

    def _post_mint_info(self, source_file_upload_id, tx_hash, token_id, mint_address):
        params = {'source_file_upload_id': source_file_upload_id, 'tx_hash': tx_hash,
                  'token_id': int(token_id), 'mint_address': mint_address}
        return self.api_client._request_with_params(POST, MINT_INFO, self.MCS_API, params, self.token, None)

    def stream_upload_file(self, file_path):
        params = {}
        params['duration'] = '525'
        params['storage_copy'] = '5'
        params['file'] = (file_path, open(file_path, 'rb'))
        return self.api_client._request_stream_upload(UPLOAD_FILE, self.MCS_API, params, self.token)

    def get_deal_detail(self, source_file_upload_id, deal_id='0'):
        params = {}
        if source_file_upload_id:
            params['source_file_upload_id'] = source_file_upload_id
        deal = self.api_client._request_with_params(GET, DEAL_DETAIL + deal_id, self.MCS_API, params, self.token, None)
        return Deal(deal["data"]["source_file_upload_deal"])

    def get_collections(self):
        res = self.api_client._request_without_params(GET, COLLECTIONS, self.MCS_API, self.token)
        return list(map(lambda collection: Collection(collection) ,res["data"]))

    def _upload_nft_metadata(self, nft):
        params = {}
        params['duration'] = '525'
        params['file_type'] = '1'
        params['wallet_address'] = self.account.address

        # params['file'] = (nft_name, json.dumps(nft))
        files = {"fileName": nft["name"], "file": json.dumps(nft)}
        return self.api_client._request_with_params(POST, UPLOAD_FILE, self.MCS_API, params, self.token, files)

        # upload = self.api_client._request_stream_upload(UPLOAD_FILE, self.MCS_API, params, self.token)
        # data = upload["data"]
        # print(data)
        # return Upload(data)

    def _approve_usdc(self, amount):
        nonce = self.w3.eth.getTransactionCount(self.account.address)
        tx = self.token_contract.functions.approve(self.payment_contract.address, amount).buildTransaction({
            'from': self.account.address,
            'nonce': nonce
        })
        signed_tx = self.w3.eth.account.signTransaction(tx, self.account._private_key)
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=CONTRACT_TIME_OUT)
        return self.w3.toHex(tx_hash)

    def _map_chain_name(self, chain_name):
        if chain_name == 'polygon.mainnet':
            return 137
        elif chain_name == 'polygon.mumbai':
            return 80001
        return -1
