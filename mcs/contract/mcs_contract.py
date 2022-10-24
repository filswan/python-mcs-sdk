from web3 import Web3
from mcs.common.constants import *
from mcs import ApiClient
from mcs.common.params import Params
from mcs.common.utils import get_contract_abi, get_amount
from web3.middleware import geth_poa_middleware


class ContractAPI(ApiClient):
    def __init__(self, rpc_endpoint, chain_name):
        self.rpc_endpoint = rpc_endpoint
        self.w3 = Web3(Web3.HTTPProvider(rpc_endpoint))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.SWAN_PAYMENT_ADDRESS = Params(chain_name).SWAN_PAYMENT_ADDRESS
        self.USDC_TOKEN = Params(chain_name).USDC_TOKEN
        self.MINT_ADDRESS = Params(chain_name).MINT_ADDRESS

    def approve_usdc(self, wallet_address, private_key, amount):
        nonce = self.w3.eth.getTransactionCount(wallet_address)
        usdc_abi = get_contract_abi(USDC_ABI)
        token = self.w3.eth.contract(self.USDC_TOKEN, abi=usdc_abi)
        decimals = token.functions.decimals().call()
        amount = amount * (10 ** decimals)
        usdc_balance = token.functions.balanceOf(wallet_address).call()
        if int(usdc_balance) < int(amount):
            print("Insufficient balance")
            return
        tx = token.functions.approve(self.SWAN_PAYMENT_ADDRESS, amount).buildTransaction({
            'from': wallet_address,
            'nonce': nonce
        })
        signed_tx = self.w3.eth.account.signTransaction(tx, private_key)
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=CONTRACT_TIME_OUT)
        return self.w3.toHex(tx_hash)

    def upload_file_pay(self, wallet_address, private_key, file_size, w_cid, rate, params):
        amount = get_amount(file_size, rate)
        nonce = self.w3.eth.getTransactionCount(wallet_address)
        swan_payment_abi = get_contract_abi(SWAN_PAYMENT_ABI)
        swan_payment = self.w3.eth.contract(self.SWAN_PAYMENT_ADDRESS, abi=swan_payment_abi)
        usdc_abi = get_contract_abi(USDC_ABI)
        token = self.w3.eth.contract(self.USDC_TOKEN, abi=usdc_abi)
        decimals = token.functions.decimals().call()
        lock_obj = {
            'id': w_cid,
            'minPayment': int(amount * (10 ** decimals)),
            'amount': int(amount * (10 ** decimals) * float(params['pay_multiply_factor'])),
            'lockTime': 86400 * params['lock_time'],
            'recipient': params['payment_recipient_address'],
            'size': file_size,
            'copyLimit': 5,
        }
        options_obj = {
            'from': wallet_address,
            'nonce': nonce
        }
        tx = swan_payment.functions.lockTokenPayment(lock_obj).buildTransaction(options_obj)
        signed_tx = self.w3.eth.account.signTransaction(tx, private_key)
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=CONTRACT_TIME_OUT)
        return self.w3.toHex(tx_hash)

    def mint_nft(self, wallet_address, private_key, nft_meta_uri):
        nonce = self.w3.eth.getTransactionCount(wallet_address)
        mint_abi = get_contract_abi(MINT_ABI)
        mint_contract = self.w3.eth.contract(self.MINT_ADDRESS, abi=mint_abi)
        option_obj = {
            'from': wallet_address,
            'nonce': nonce
        }
        tx = mint_contract.functions.mintUnique(wallet_address, str(nft_meta_uri)).buildTransaction(option_obj)
        signed_tx = self.w3.eth.account.signTransaction(tx, private_key)
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=CONTRACT_TIME_OUT)
        result = mint_contract.events.TransferSingle().processReceipt(receipt)
        id = result[0]['args']['id']
        token_id = int(id)
        return self.w3.toHex(tx_hash), token_id
