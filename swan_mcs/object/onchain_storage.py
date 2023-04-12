import json


class Upload:
    def __init__(self, upload_data):
        self.source_file_upload_id = upload_data["source_file_upload_id"]
        self.payload_cid = upload_data["payload_cid"]
        self.ipfs_url = upload_data["ipfs_url"]
        self.file_size = upload_data["file_size"]
        self.w_cid = upload_data["w_cid"]
        self.status = upload_data["status"]

    def pay(self, amount=''):
        pass

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Deal:
    def __init__(self, deal_data):
        self.deal_id = deal_data.get("deal_id", None)
        self.message_cid = deal_data.get("message_cid", None)
        self.deal_cid = deal_data["deal_cid"]
        self.height = deal_data["height"]
        self.piece_cid = deal_data["piece_cid"]
        self.verified_deal = deal_data["verified_deal"]
        self.storage_price_per_epoch = deal_data["storage_price_per_epoch"]
        self.signature = deal_data["signature"]
        self.signature_type = deal_data["signature_type"]
        self.created_at = deal_data["created_at"]
        self.piece_size_format = deal_data["piece_size_format"]
        self.start_height = deal_data["start_height"]
        self.end_height = deal_data["end_height"]
        self.client = deal_data["client"]
        self.client_collateral_format = deal_data["client_collateral_format"]
        self.provider = deal_data["provider"]
        self.provider_tag = deal_data["provider_tag"]
        self.verified_provider = deal_data["verified_provider"]
        self.provider_collateral_format = deal_data["provider_collateral_format"]
        self.status = deal_data["status"]
        self.network_name = deal_data["network_name"]
        self.storage_price = deal_data["storage_price"]
        self.ipfs_url = deal_data["ipfs_url"]
        self.file_name = deal_data["file_name"]
        self.w_cid = deal_data["w_cid"]
        self.car_file_payload_cid = deal_data["car_file_payload_cid"]
        self.locked_at = deal_data["locked_at"]
        self.locked_fee = deal_data["locked_fee"]
        self.unlocked = deal_data["unlocked"]

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

class SourceFile:
    def __init__(self, file_data):
        self.source_file_upload_id = file_data["source_file_upload_id"]
        self.file_name = file_data["file_name"]
        self.file_size = file_data["file_size"]
        self.upload_at =  file_data["upload_at"]
        self.duration =  file_data["duration"]
        self.ipfs_url = file_data["ipfs_url"]
        self.pin_status =  file_data["pin_status"]
        self.pay_amount =  file_data["pay_amount"]
        self.status =  file_data["status"]
        self.note =  file_data["note"]
        self.is_free =  file_data["is_free"]
        self.is_minted =  file_data["is_minted"]
        self.refunded_by_self =  file_data["refunded_by_self"]
        self.offline_deal =  file_data["offline_deal"]
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

class Collection:
    def __init__(self, collection_data):
        self.id = collection_data["id"]
        self.address = collection_data["address"]

        self.name = collection_data["name"]
        self.description = collection_data["description"]
        self.image_url = collection_data["image_url"]
        self.external_link = collection_data["external_link"]
        self.seller_fee = collection_data["seller_fee"]
        self.wallet_id = collection_data["wallet_id"]
        self.wallet_id_recipient = collection_data["wallet_id_recipient"]
        self.wallet_recipient = collection_data["wallet_recipient"]
        self.is_default = collection_data["is_default"]

        self.tx_hash = collection_data["tx_hash"]
        self.create_at = collection_data["create_at"]
        self.update_at = collection_data["update_at"]

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

class Payment:
    def __init__(self, payment_data):
        self.w_cid = payment_data["w_cid"]
        self.pay_amount = payment_data["pay_amount"]
        self.pay_tx_hash = payment_data["pay_tx_hash"]
        self.token_address = payment_data["token_address"]

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)