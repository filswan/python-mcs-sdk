# Multichain Storage SDK - Python

[![Made by FilSwan](https://img.shields.io/badge/made%20by-FilSwan-green.svg)](https://www.filswan.com/)
[![Chat on discord](https://img.shields.io/badge/join%20-discord-brightgreen.svg)](https://discord.com/invite/KKGhy8ZqzK)

A python software development kit for the Multi-Chain Storage(MCS) https://www.multichain.storage service. It provides a convenient interface for working with the MCS API. 

# Table of Contents <!-- omit in toc -->

- [Getting Started](#-Getting-Started)
  - [Installation](#Installation)
- [Examples](#-Examples)
- [Functions](#ℹ️-Functions)
  - [For Buckets Storage](#For-Buckets-Storage)
- [Contributing](#contributing)

## 🆕 Getting Started

### Installation

-  via _pip_ (Recommended):

 ```
pip install python-mcs-sdk
 ```

-  Build from source (optional)

 ```
git clone https://github.com/filswan/python-mcs-sdk.git
git checkout main
pip install -r requirements.txt
 ```

### Setup Credentials

api_key/access_token can be found in https://www.multichain.storage/#/api_key, make sure save your APIKey and Access Token after you have generated it, you will not find it again after you created it

**Authentication**

 ```python
from swan_mcs import APIClient
if __name__ == '__main__':
    api_key="<API_KEY>"
    access_token="<ACCESS_TOKEN>"
    mcs_api = APIClient(api_key)
 ```

## 👨‍💻 Examples

### Bucket Storage

- Create a bucket

```python
from swan_mcs import BucketAPI
    bucket_client = BucketAPI(mcs_api)
    bucket_data = bucket_client.create_bucket('YOUR_BUCKET_NAME')
    print(bucket_data)
```

-  Upload a file to the bucket

```python
    # file_path is the path relative to the current file
    # object_name is your target path. e.g: 'FOLDER_NAME/FILENAME'
    file_data = bucket_client.upload_file('YOUR_BUCKET_NAME', 'OBJECT_NAME' , 'FILE_PATH') 
    print(file_data.to_json())
```

* Pay for the storage contract

Please move forward for [How to pay for the storage](https://docs.filswan.com/multichain.storage/developer-quickstart/sdk/python-mcs-sdk/onchain-storage/advanced-usage)

For more examples, please see the [SDK documentation.](https://docs.filswan.com/multi-chain-storage/developer-quickstart/sdk)

## ℹ️ Functions

This SDK has the following functionalities:

### For Buckets Storage

---

* **POST** Create a bucket
* **POST** Create a folder
* **POST** Upload File to the bucket
* **POST** Rename bucket
* **GET** Delete bucket
* **GET** Bucket List
* **GET** File List
* **GET** File information
* **GET** Delete File

## Contributing

Feel free to join in and discuss. Suggestions are welcome! [Open an issue](https://github.com/filswan/python-mcs-sdk/issues) or [Join the Discord](https://discord.com/invite/KKGhy8ZqzK)!

### Sponsors

Filecoin Foundation sponsors this project

[Flink SDK - A data provider offers Chainlink Oracle service for Filecoin Network ](https://github.com/filecoin-project/devgrants/issues/463)

<img src="https://github.com/filswan/flink/blob/main/filecoin.png" width="200">
