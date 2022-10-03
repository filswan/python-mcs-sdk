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
web3_api : <WEB3_API>
```

### Basic functions
Approve wallet (to spend token)

```python
def approve_usdc():
    w3_api = ContractAPI(web3_api)
    w3_api.approve_usdc(wallet_address,
                        private_key, "1")
```

Example of uploading a single file using the MCS SDK. 
```diff
- (Note that the mcs mainnet currently have 10GB of free upload amount for each wallet per month. While you can still manually pay for the upload, it is not recommanded as the lockedpayment might not be able to unlock under this circumstance. This code is only demonstration purpose and should not be used to upload file on mcs mainnet, the upload function covers free upload is under `upload/free_upload.py`)
```

```python
def upload_file_pay(wallet_info):
    wallet_address = wallet_info['wallet_address']
    private_key = wallet_info['private_key']
    web3_api = wallet_info['web3_api']

    w3_api = ContractAPI(web3_api)
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

## Testing
You can use the pytest functions provided under the test directory to test the functionality of python mcs sdk. \

`test`

## Documentation

For more examples please see the [SDK documentation](https://docs.filswan.com/multi-chain-storage/developer-quickstart/sdk) or the example directory in the [sdk-test repository](https://github.com/filswan/python-mcs-sdk/tree/main/test), which contains sample code for all SDK functionalities

# Contributing

Feel free to join in and discuss. Suggestions are welcome! [Open an issue](https://github.com/filswan/python-mcs-sdk/issues) or [Join the Discord](https://discord.com/invite/KKGhy8ZqzK)!

## Sponsors

This project is sponsored by Filecoin Foundation

[Flink SDK - A data provider offers Chainlink Oracle service for Filecoin Network ](https://github.com/filecoin-project/devgrants/issues/463)

<img src="https://github.com/filswan/flink/blob/main/filecoin.png" width="200">
