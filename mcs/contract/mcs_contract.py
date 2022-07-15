from web3 import Web3
from mcs.common.constants import *
from mcs import ApiClient
from mcs.common.utils import get_contract_abi, get_amount
from web3.middleware import geth_poa_middleware


class ContractAPI(ApiClient):
    def __init__(self, web3_api, ):
        self.web3_api = web3_api
        self.w3 = Web3(Web3.HTTPProvider(web3_api))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    def approve_usdc(self, wallet_address, private_key, amount):
        amount = self.w3.toWei(amount, 'ether')
        nonce = self.w3.eth.getTransactionCount(wallet_address)
        usdc_abi = get_contract_abi(USDC_ABI)
        token = self.w3.eth.contract(USDC_TOKEN, abi=usdc_abi)
        usdc_balance = token.functions.balanceOf(wallet_address).call()
        if usdc_balance < amount:
            print("Insufficient balance")
            return
        tx = token.functions.approve(USDC_SPENDER, amount).buildTransaction({
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
        swan_payment = self.w3.eth.contract(SWAN_PAYMENT_ADDRESS, abi=swan_payment_abi)
        lock_obj = {
            'id': w_cid,
            'minPayment': self.w3.toWei(amount, 'ether'),
            'amount': int(self.w3.toWei(amount, 'ether') * float(params['PAY_MULTIPLY_FACTOR'])),
            'lockTime': 86400 * params['LOCK_TIME'],
            'recipient': params['PAYMENT_RECIPIENT_ADDRESS'],
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
        mint_contract = self.w3.eth.contract(MINT_ADDRESS, abi=mint_abi)
        option_obj = {
            'from': wallet_address,
            'nonce': nonce
        }
        tx = mint_contract.functions.mintData(wallet_address, str(nft_meta_uri)).buildTransaction(option_obj)
        signed_tx = self.w3.eth.account.signTransaction(tx, private_key)
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        token_id = mint_contract.functions.totalSupply().call()
        self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=CONTRACT_TIME_OUT)
        return self.w3.toHex(tx_hash), token_id
