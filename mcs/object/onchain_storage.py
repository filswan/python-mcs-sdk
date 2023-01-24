import json

class PaymentInfo:
    def __init__(self, onchain_data):
        self.w_cid = onchain_data['w_cid']
        self.pay_amount = onchain_data['pay_amount']
        self.pay_txhash = onchain_data['pay_tx_hash']
        self.token_address = onchain_data['token_address']

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

class Deal:
    def __init__(self, onchain_data):
        self.id = onchain_data['id']
        self.car_file_id = onchain_data['car_file_id']
        self.deal_cid = onchain_data['deal_cid']
        self.miner_id = onchain_data['miner_id']
        self.verified = onchain_data['verified']
        self.start_epoch = onchain_data['start_epoch']
        self.sender_wallet_id = onchain_data['sender_wallet_id']
        self.status = onchain_data['status']
        self.deal_id = onchain_data['deal_id']
        self.onchain_status = onchain_data['on_chain_status']
        self.unlock_txhash = onchain_data['unlock_tx_hash']
        self.unlock_at = onchain_data['unlock_at']
        self.note = onchain_data['note']
        self.network_id = onchain_data['network_id']
        self.created_at = onchain_data['create_at']
        self.updated_at = onchain_data['update_at']
        self.miner_fid = onchain_data['miner_fid']

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

class SourceFile:
    def __init__(self, onchain_data):
        self.source_file_upload_id = onchain_data['source_file_upload_id'] if 'source_file_upload_id' in onchain_data else None
        self.w_cid = onchain_data['w_cid'] if 'w_cid' in onchain_data else None
        self.file_name = onchain_data['file_name'] if 'file_name' in onchain_data else None
        self.file_size = onchain_data['file_size'] if 'file_size' in onchain_data else None
        self.upload_at = onchain_data['upload_at'] if 'upload_at' in onchain_data else None
        self.duration = onchain_data['duration'] if 'duration' in onchain_data else None
        self.ipfs_url = onchain_data['ipfs_url'] if 'ipfs_url' in onchain_data else None
        self.pin_status = onchain_data['pin_status'] if 'pin_status' in onchain_data else None
        self.pay_amount = onchain_data['pay_amount'] if 'pay_amount' in onchain_data else None
        self.status = onchain_data['status'] if 'status' in onchain_data else None
        self.note = onchain_data['note'] if 'note' in onchain_data else None
        self.is_free = onchain_data['is_free'] if 'is_free' in onchain_data else None
        self.is_minted = onchain_data['is_minted'] if 'is_minted' in onchain_data else None 
        self.token_id = onchain_data['token_id'] if 'token_id' in onchain_data else None
        self.mint_address = onchain_data['mint_address'] if 'mint_address' in onchain_data else None
        self.nft_txhash = onchain_data['nft_tx_hash'] if 'nft_tx_hash' in onchain_data else None 
        self.refunded_by_self = onchain_data['refunded_by_self'] if 'refunded_by_self' in onchain_data else None
        self.offline_deals = [] if 'offline_deal' in onchain_data else None
        if self.offline_deals:
            for deal in onchain_data['offline_deal']:
                self.offline_deals.append(Deal(deal))
    
    def put_payment_info(self, payment_info):
        self.payment_info : PaymentInfo = payment_info

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)