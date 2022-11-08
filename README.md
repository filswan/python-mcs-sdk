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
- **GET**       list of files uploaded
- **GET**       files by cid
- **GET**       status from filecoin

## Prequisites

- [web3](https://pypi.org/project/web3/) - web3 python package to process contract
- Polygon Mainnet Wallet - [Metamask Tutorial](https://docs.filswan.com/getting-started/beginner-walkthrough/public-testnet/setup-metamask)
- Polygon Mainnet RPC - [Signup via Alchemy](https://www.alchemy.com/)
- Polygon RPC endpoint - https://polygon-rpc.com/ (you will also need USDC and MATIC balance to use this SDK.)

- [pytest](https://docs.pytest.org/en/7.1.x/) (for testing purpose)
- [requests](https://pypi.org/project/requests/) for requesting mcs api
- [requests-toolbelt](https://pypi.org/project/requests-toolbelt/) for stream upload
- [python-dotenv](https://pypi.org/project/python-dotenv/) to read `.env` file that is used to store wallet info
 
# MCS API

For more information about the API usage, check out the MCS API documentation (https://docs.filswan.com/development-resource/mcp-api).

# Usage

Instructions for developers working with MCS SDK and API.

## Installation

### Method 1. Using Github
Install python sdk from github (checkout to the main branch if not alreayd on) and install requirements using pip

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

### Set Up Wallet Infomations
First you should set up your wallet address, private key and web3 api. There can be put into `.env_main` file under the same directory (under test directory for using pytest functions). `python-dotenv` will only look for file that named exactly as `.env_main` under the current directory.
```
wallet_address="<WALLET_ADDRESS>"
private_key="<PRIVATE_KEY>"
rpc_endpoint="<RPC_ENDPOINT>"
```

Then you can use `dotenv` package to load the `.env`.
```python
import os
from dotenv import load_dotenv

load_dotenv("<.env_file_name>")

private_key = os.getenv('private_key')
rpc_endpoint = os.getenv('rpc_endpoint')
```

Additionally `wallet address` can be retrieved using `private key` through web3py pacakge.
```python
from web3 import Web3

w3 = Web3(Web3.HTTPProvider(<rpc_endpoint>))
wallet_address = w3.eth.account.privateKeyToAccount(<private_key>).address
print(wallet_address)
```

### Get MCS jwt token
To access main functions of MCS, you will need to complete authorization with jwt toke. \
The function `MCS.get_jwt_token` allows authorization using signature generate with `wallet_address` and `private_key`. \
By initialize a new `MCS` instance and calling the `get_jwt_token()`, the token will store within the current `MCS` instance 
for the use in the current session. (Note that MCS currently only support `polygon.mainnet` which is the only possible chain_name
to login into)

example:
```
from mcs import McsAPI
from mcs.common.params import Params

api = McsAPI(Params().MCS_API)
jwt_token = api.get_jwt_token(wallet_address, private_key, "polygon.mainnet")
print(api.token)
```

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


### Basic functions

Import neccessary modules

```python
from mcs import McsAPI
from mcs import ContractAPI
from mcs.common.params import Params
from mcs.common.utils import get_amount
```

Create a class for accesing MCS API and Contract

```python
class upload():
```

Load wallet and upload informations.

```python 
def __init__(self, chain_name, wallet_address, private_key, rpc_endpoint, file_path):
  self.chain_name = chain_name
  self.wallet_address = wallet_address
  self.private_key = private_key
  self.rpc_endpoint = rpc_endpoint
  self.file_path = file_path
  self.upload_response = None
  self.payment_tx_hash = None

  self.api = McsAPI(Params(self.chain_name).MCS_API)
  self.api.get_jwt_token(self.wallet_address, self.private_key, self.chain_name)
  self.w3_api = ContractAPI(self.rpc_endpoint, self.chain_name)
```

Approve wallet (to spend token)

```python
def approve_usdc():
  self.w3_api.approve_usdc(self.wallet_address, self.private_key, amount)
```

Example of uploading a single file using the MCS SDK. (Note that the mcs mainnet currently have 10GB of free upload amount for each wallet per month. While you can still manually pay for the upload, it is not recommanded as the lockedpayment might not be able to unlock under this circumstance.)

```python
def stream_upload(self):
  upload_file = self.api.stream_upload_file(self.wallet_address, self.file_path)
  file_data = upload_file["data"]
  need_pay = 0
  if file_data["status"] == "Free":
    self.upload_response = file_data

  else:
    self.upload_response = file_data
    need_pay = 1
    return file_data, need_pay
```

For free upload, the upload api will return `is_free` parameter, while this is true the file does not require to be paid using the `SwanPayment contract`. However, this free_upload only applies to the first 10GB of upload per month, and file larger than 10GB will needs to be paid. (Files cannot be partially free uploaded)

An example for payment:
```python
def pay(self):
  file_size, w_cid = self.upload_response['file_size'], self.upload_response['w_cid']
  params = self.api.get_params()["data"]
  rate = self.api.get_price_rate()["data"]
  # payment
  try:
    self.payment_tx_hash = self.w3_api.upload_file_pay(self.wallet_address, 
      self.private_key, file_size, w_cid, rate, params)
  except Exception as e:
    logging.error(str(e))
    return 'payment failed: ' + str(e)

  return payment_tx_hash
```

The estimated amount for payment can be computed after uploading the file.
```python
def estimate_amount(self):
        file_size = self.upload_response['file_size']
        rate = self.api.get_price_rate()["data"]
        amount = get_amount(file_size, rate)
        return amount
```

## Testing
You can use the pytest functions provided under the test directory to test the functionality of python mcs sdk. (note that testing mcs on polygon mainnet will cost)

- `test_mcs_api`: Test the mcs backend api for getting params, uploads and access deal infos. This also allows to check whether mcs backend apis are functioning.
- `test_api_response`: Test if the apis and mcs contracts returns expected responses.
- `test_simple_upload`: Test the pre-build `MCSUpload` class for simple upload.


## Documentation

For more examples please see the [SDK documentation](https://docs.filswan.com/multi-chain-storage/developer-quickstart/sdk) or the example directory in the [sdk-test repository](https://github.com/filswan/python-mcs-sdk/tree/main/test), which contains sample code for all SDK functionalities

# Contributing

Feel free to join in and discuss. Suggestions are welcome! [Open an issue](https://github.com/filswan/python-mcs-sdk/issues) or [Join the Discord](https://discord.com/invite/KKGhy8ZqzK)!

## Sponsors

This project is sponsored by Filecoin Foundation

[Flink SDK - A data provider offers Chainlink Oracle service for Filecoin Network ](https://github.com/filecoin-project/devgrants/issues/463)

<img src="https://github.com/filswan/flink/blob/main/filecoin.png" width="200">
