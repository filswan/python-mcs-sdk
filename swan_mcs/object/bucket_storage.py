import json


class Bucket:
    def __init__(self, bucket_data):
        self.deleted_at = bucket_data["deleted_at"]
        self.updated_at = bucket_data["updated_at"]
        self.created_at = bucket_data["created_at"]
        self.file_number = bucket_data["file_number"]
        self.bucket_name = bucket_data["bucket_name"]
        self.is_deleted = bucket_data["is_deleted"]
        self.is_active = bucket_data["is_active"]
        self.is_free = bucket_data["is_free"]
        self.size = bucket_data["size"]
        self.max_size = bucket_data["max_size"]
        self.address = bucket_data["address"]
        self.bucket_uid = bucket_data["bucket_uid"]

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class File:
    def __init__(self, file_data, gateway = 'https://ipfs.io'):
        self.name = file_data["name"]
        self.address = file_data["address"]
        self.bucket_uid = file_data["bucket_uid"]
        self.filehash = file_data["file_hash"]
        self.prefix = file_data["prefix"]
        self.size = file_data["size"]
        self.payloadCid = file_data["payload_cid"]
        self.ipfs_url = gateway + '/ipfs/' + file_data["payload_cid"] # think there is an issue here
        self.pin_status = file_data["pin_status"]
        self.is_deleted = file_data["is_deleted"]
        self.is_folder = file_data["is_folder"]
        self.id = file_data["id"]
        self.updated_at = file_data["updated_at"]
        self.created_at = file_data["created_at"]
        self.deleted_at = file_data["deleted_at"]
        self.gateway = gateway
        self.object_name = file_data["object_name"]
        self.type = file_data["type"]

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
