import os

from mcs import APIClient, BucketAPI


def upload_replace_file(file_path, bucket_name, dest_file_path):
    """
    Upload a file by file path, bucket name and the target path
    :param file_path: the source file path
    :param bucket_name: the bucket name user want to upload
    :param dest_file_path: the destination of the file you want to store exclude the bucket name
    :return: File Object
    """
    mcs_api = APIClient(api_key, access_token,network)
    bucket_client = BucketAPI(mcs_api)
    # check if file exist
    file_data = bucket_client.get_file(bucket_name, dest_file_path)
    if file_data:
        print("File exist,replace file: %s" % file_path)
        bucket_client.delete_file(bucket_name, dest_file_path)
    file_data = bucket_client.upload_file(bucket_name, dest_file_path, file_path)
    return file_data


if __name__ == '__main__':
    api_key = "XXXX"
    access_token = "xxxxxxx"
    network = "polygon.mainnet"
    file_path = 'data/apple.jpeg'
    # file_path is the path relative to the current file
    # object_name is your target path
    mcs_file = upload_replace_file(file_path, "swan",
                                   os.path.join("0x165CD37b4C644C2921454429E7F9358d18A45e14", "apple.jpeg"))
