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

[web3](https://pypi.org/project/web3/) \
Polygon Mumbai Testnet Wallet - [Metamask Tutorial](https://docs.filswan.com/getting-started/beginner-walkthrough/public-testnet/setup-metamask) \
Polygon Mumbai Testnet RPC - [Signup via Alchemy](https://www.alchemy.com/)

You will also need Testnet USDC and MATIC balance to use this SDK. [Swan Faucet Tutorial](https://docs.filswan.com/development-resource/swan-token-contract/acquire-testnet-usdc-and-matic-tokens) \
[pytest](https://docs.pytest.org/en/7.1.x/) (for testing purpose)

# MCS API

For more information about the API usage, check out the MCS API documentation (https://docs.filswan.com/development-resource/mcp-api).

# Usage

Instructions for developers working with MCS SDK and API.

## Installation

Install using pip
```
$ pip install -r requirements.txt
```

## Getting Started

First you should set your wallet address, private key and web3 api.

```python
wallet_info = {
  'wallet_address' : <WALLET_ADDRESS>
  'private_key' : <PRIVATE_KEY>
  'web3_api' : <WEB3_API>
}
```

Approve wallet (to spend token)

'''python
def approve_usdc():
    w3_api = ContractAPI(web3_api)
    w3_api.approve_usdc(wallet_address,
                        private_key, "1")
'''

Example of uploading a single file using the MCS SDK.

```python
def upload_file_pay(wallet_info):
    wallet_address = wallet_info['wallet_address']
    private_key = wallet_info['private_key']
    web3_api = wallet_info['web3_api']

    w3_api = ContractAPI(web3_api)
    api = McsAPI()
    # upload file to mcs
    filepath = "/images/log_mcs.png"
    father_path = os.path.abspath(os.path.dirname(__file__))
    upload_file = api.upload_file(wallet_address, father_path + filepath)
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

## Documentation

For more examples please see the [SDK documentation](https://docs.filswan.com/multi-chain-storage/developer-quickstart/sdk) or the example directory in the [sdk-test repository](https://github.com/filswan/python-mcs-sdk/tree/main/test), which contains sample code for all SDK functionalities

# Contributing

Feel free to join in and discuss. Suggestions are welcome! [Open an issue](https://github.com/filswan/python-mcs-sdk/issues) or [Join the Discord](https://discord.com/invite/KKGhy8ZqzK)!

## Sponsors

This project is sponsored by Filecoin Foundation

[Flink SDK - A data provider offers Chainlink Oracle service for Filecoin Network ](https://github.com/filecoin-project/devgrants/issues/463)

<img src="https://github.com/filswan/flink/blob/main/filecoin.png" width="200">
