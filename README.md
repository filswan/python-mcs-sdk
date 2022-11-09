# python-mcs-sdk

[![Made by FilSwan](https://img.shields.io/badge/made%20by-FilSwan-green.svg)](https://www.filswan.com/)
[![Chat on discord](https://img.shields.io/badge/join%20-discord-brightgreen.svg)](https://discord.com/invite/KKGhy8ZqzK)

# Table of Contents <!-- omit in toc -->

- [Introduction](#introduction)
  - [Prerequisites](#prerequisites)
- [MCS API](#mcs-api)
- [Usage](#usage)
  - [Installation](#installation)
  - [Getting Started](#getting-started)
  - [Testing](#testing)
  - [Documentation](#documentation)
- [Contributing](#contributing)

# Introduction

A python software development kit for the Multi-Chain Storage (MCS) https://www.multichain.storage/ service. It provides a convenient interface for working with the MCS API. This SDK has the following functionalities:

- **POST**    upload file to Filswan IPFS gate way
- **POST**    make payment to swan filecoin storage gate way
- **POST**    mint asset as NFT
- **GET**     list of files uploaded
- **GET**     files by cid
- **GET**     status from filecoin

## Prequisites

- [web3](https://pypi.org/project/web3/) - web3 python package to process contract 
- Polygon Mainnet Wallet - [Metamask Tutorial](https://docs.filswan.com/getting-started/beginner-walkthrough/public-testnet/setup-metamask)
- Polygon Mainnet RPC endpoint - [Signup via Alchemy](https://www.alchemy.com/) or use https://polygon-rpc.com/ (you will also need USDC and MATIC balance to use this SDK.)

# MCS API

For more information about the API usage, check out the MCS API documentation (https://docs.filswan.com/development-resource/mcp-api).

# Usage

Instructions for developers working with MCS SDK and API.

## Installation

### Method 1. Using Github
Install python sdk from github (checkout to main branch for mainnet support) and install requirements using pip

```
git clone https://github.com/filswan/python-mcs-sdk.git
git checkout main
pip install -r requirements.txt
```

### Method 2. Using Pip
Install python sdk use pip https://pypi.org/project/python-mcs-sdk/

```
pip install python-mcs-sdk
```

## Getting Started

This is a demo for users to use the simplified MCS upload functions `MCSUpload`. For the complete [documentations](#documentation).

### MCS upload
You can use the `MCSUpload` class in `upload/mcs_upload.py` to upload file or as an simple example for accessing MCS api and smart contract.

The `MCSUpload` contains functions:
- `__init__()`: 
  - parameters:  `chain_name`, `wallet_address`, `private_key`, `rpc_endpoint`, `file_path`
  - initialize the upload function using wallet infos and file_path
- `approve_token()`:
  - parameters: `amount`
  - return: txhash for approve
  - change the approved amount (this value will be reset to the amount rather than increment)
- `stream_upload()`:
  - return: api response from mcs upload
  - Upload file to mcs, this function will return `is_free` variable and the payment needs not require payment when `need_pay==0`
- `estimate_amount()`:
  - return: estimated lockin payment
  - can be used to check the payment amount after upload file (upload will not be processed until the payment is made through contract)
- `pay()`:
  - return: payment success / payment failed with error message
  - this function call the payment contract to pay for the currently processing upload (info stored in upload_response)
- `mint()`:
  - parameters: `file_name`
  - return: `tx_hash`, `token_id`, mcs mint update api response
  - this functions allows to mint nft to open sea

### Create File
Let's create two files `.env_main` to store wallet informations and `demo.py` to run the demo code.

### Set Up Wallet Infomations
First you should set up your wallet address, private key and web3 api. (They can be put into `.env` file for security, reade )
```
wallet_address="<WALLET_ADDRESS>"
private_key="<PRIVATE_KEY>"
rpc_endpoint="<RPC_ENDPOINT>"
```

### Initialize Upload
To start upload, we need to create an instance of the `MCSUpload` class. Which requires `chain_name`, `wallet_address`, `private_key` and `file_path` as 
parameters. The upload process requires user login into the MCS API using wallet address. Python MCS SDK can handle this process automatically when initialing
a MCSUpload.

```python
from mcs import McsAPI

file_path = <absolute path of the file>

upload = MCSUpload("polygon.mainnet", wallet_address, private_key, rpc_endpoint, file_path)
```

### Upload File
To upload the file to MCS, we need to call the `stream_upload()` function.

```python
file_data, need_pay = upload.stream_upload()
```

The upload function upload the file to IPFS server. MCS currently have 10GB of free upload per month for each wallet. The `need_pay` will indicates if a file is under 
the coverage of free upload. When `need_pay == 1` then the file needs to paid and its free when `need_pay == 0`.

### Approve Token
Before processing payment we need to approve enough token for the upload payment and gas fee. You don't need to approve any token if the upload is free. You can also choose how much you want to approve base on the estimated price.

```python
upload.approve_token(<amount>)
```

### Estimate Payment
The estimated payment can be accessed using `estimate_amount()` function.

```python
print(upload.estimate_amount())
```

### Payment
Currently on MCS mainnet, user only needs to pay if the upload surpass the free upload coverage. However, user can still force a payment after upload (This is not recommanded).

```python
if need_pay:
  upload.pay()
```

### Full Demo Code
Full demo code for testing, you will needs to add your own wallet infos and add the `amount` and `file_path` in the following script.

```python
from mcs.upload.mcs_upload import MCSUpload

if __name__ == '__main__':

    # Load wallet info
    wallet_address, private_key, rpc_endpoint = <wallet_address>, <private_key>, <rpc_endpoint>

    # Load file path
    file_path = <absolute path>

    # Upload file
    upload = MCSUpload("polygon.mainnet", wallet_address, private_key, rpc_endpoint, file_path)
    file_data, need_pay = upload.stream_upload()

    # Process payment
    if need_pay:
        upload.approve_token(<amount>)
        upload.pay()
    
    print('Upload successfully')
```


## Testing
You can use the pytest functions provided under the test directory to test the functionality of python mcs sdk. (note that testing mcs on polygon mainnet will cost real currency)

- `test_mcs_api`: Test the mcs backend api for getting params, uploads and access deal infos. This also allows to check whether mcs backend apis are functioning.
- `test_api_response`: Test if the apis and mcs contracts returns expected responses.
- `test_simple_upload`: Test the pre-build `MCSUpload` class for simple upload.


## Documentation

For more examples please see the [SDK documentation](https://docs.filswan.com/multi-chain-storage/developer-quickstart/sdk) or \
the test cases in the [sdk-test repository](https://github.com/filswan/python-mcs-sdk/tree/main/test), which contains sample code for all SDK functionalities

# Contributing

Feel free to join in and discuss. Suggestions are welcome! [Open an issue](https://github.com/filswan/python-mcs-sdk/issues) or [Join the Discord](https://discord.com/invite/KKGhy8ZqzK)!

## Sponsors

This project is sponsored by Filecoin Foundation

[Flink SDK - A data provider offers Chainlink Oracle service for Filecoin Network ](https://github.com/filecoin-project/devgrants/issues/463)

<img src="https://github.com/filswan/flink/blob/main/filecoin.png" width="200">
