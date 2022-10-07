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

A python software development kit for the Multi-Chain Storage (MCS) https://mcs.filswan.com service. It provides a convenient interface for working with the MCS API. This SDK has the following functionalities:

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
- Polygon RPC endpoint - https://polygon-rpc.com/

You will also need Testnet USDC and MATIC balance to use this SDK. [Swan Faucet Tutorial](https://docs.filswan.com/development-resource/swan-token-contract/acquire-testnet-usdc-and-matic-tokens)
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
$ git clone https://github.com/filswan/python-mcs-sdk.git
$ git checkout main
$ pip install -r requirements.txt
```

## Getting Started

### Set Up Wallet Infomations
First you should set your wallet address, private key and web3 api. There can be put into a .env file under the same directory (under test directory for using pytest functions). `python-dotenv` will only look for file that named exactly as .env under the current directory.
```
wallet_address : <WALLET_ADDRESS>
private_key : <PRIVATE_KEY>
rpc_endpoint : <RPC_ENDPOINT>
```

### MCS upload
You can use the `MCSUpload` class in `upload/mcs_upload.py` to upload file or as an example for accessing MCS api and smart contract.

The `MCSUpload` contains functions:
- `__init__()`: 
  - parameters:  `wallet_address`, `private_key`, `rpc_endpoint`, `file_path`
  - initialize the upload function using wallet infos and file_path
- `change_file()`:
  - parameters: `file_path`
  - return: the current file path
  - changed the file_path for upload
- `check_allowance()`:
  - change allowance amount of the wallet
  - return the current approved amount of the wallet
- `approve_token()`:
  - parameters: `amount`
  - return: txhash for approve
  - change the approved amount (this value will be reset to the amount rather than increment)
- `free_upload()`:
  - return: result of free upload
  - this function upload and pay for the upload automatically. file will not be paid if the reutnr status from api is free (you can also upload manually).
- `upload()`:
  - return: api response from mcs upload
  - upload the file and get returned payment information
- `stream_upload()`:
  - return: api response from mcs upload
  - use stream upload for large file
- `estimate_amount()`:
  - return: estimated lockin payment
  - can be used to check the payment amount after upload file (free upload will skip this and pay automatically)
- `pay()`:
  - return: payment success / payment failed with error message
  - this function call the payment contract to pay for the currently processing upload (info stored in upload_response)
- `mint()`:
  - parameters: `file_name`
  - return: `tx_hash`, `token_id`, mcs mint update api response
  - this functions allows to mint nft to open sea


### Basic functions
Approve wallet (to spend token)

```python
def approve_usdc():
    w3_api = ContractAPI(rpc_endpoint)
    w3_api.approve_usdc(wallet_address,
                        private_key, "1")
```

Example of uploading a single file using the MCS SDK. (Note that the mcs mainnet currently have 10GB of free upload amount for each wallet per month. While you can still manually pay for the upload, it is not recommanded as the lockedpayment might not be able to unlock under this circumstance. This code is only demonstration purpose and should not be used to upload file on mcs mainnet, the free upload is under `upload/free_upload.py`)

```python
def upload_file_pay(wallet_info):
    wallet_address = wallet_info['wallet_address']
    private_key = wallet_info['private_key']
    rpc_endpoint = wallet_info['rpc_endpoint']

    w3_api = ContractAPI(rpc_endpoint)
    api = McsAPI()
    # upload file to mcs
    filepath = "/images/log_mcs.png"
    parent_path = os.path.abspath(os.path.dirname(__file__))
    upload_file = api.upload_file(wallet_address, parent_path + filepath)
    file_data = upload_file["data"]
    payload_cid, source_file_upload_id, nft_uri, file_size, w_cid = file_data['payload_cid'], file_data[
        'source_file_upload_id'], file_data['ipfs_url'], file_data['file_size'], file_data['w_cid']
    # get the global variable
    params = api.get_params()["data"]
    # get filcoin price
    rate = api.get_price_rate()["data"]
    # upload file and pay contract
    w3_api.upload_file_pay(wallet_address, private_key, file_size, w_cid, rate, params)

if __name__ == "__main__":
  upload_file_pay(wallet_info)
```

For free upload, the upload api will return `is_free` parameter, while this is true the file does not require to be paid using the `SwanPayment contract`. However, this free_upload only applies to the first 10GB of upload per month, and file larger than 10GB will needs to be paid. (Files cannot be partially free uploaded)

An example to use free upload:
```python
def free_upload():
        file_data = upload()
        if file_data['status'] == 'Free':
            return 'free upload'
        result = pay()
        return result
```

## Testing
You can use the pytest functions provided under the test directory to test the functionality of python mcs sdk.

- `test_mcs_api`: Test the mcs backend api for getting params, uploads and access deal infos. This also allows to check whether mcs backend apis are functioning.
- `test_contract_api`: Test contract for payment. Can be used as example of calling contract functions for payment.
- `test_api_response`: Test if the apis returns expected responses.


## Documentation

For more examples please see the [SDK documentation](https://docs.filswan.com/multi-chain-storage/developer-quickstart/sdk) or the example directory in the [sdk-test repository](https://github.com/filswan/python-mcs-sdk/tree/main/test), which contains sample code for all SDK functionalities

# Contributing

Feel free to join in and discuss. Suggestions are welcome! [Open an issue](https://github.com/filswan/python-mcs-sdk/issues) or [Join the Discord](https://discord.com/invite/KKGhy8ZqzK)!

## Sponsors

This project is sponsored by Filecoin Foundation

[Flink SDK - A data provider offers Chainlink Oracle service for Filecoin Network ](https://github.com/filecoin-project/devgrants/issues/463)

<img src="https://github.com/filswan/flink/blob/main/filecoin.png" width="200">
