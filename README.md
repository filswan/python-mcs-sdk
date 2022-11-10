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

- **POST**    upload file to Filswan IPFS gateway
- **POST**    make payment to swan filecoin storage gateway
- **POST**    mint asset as NFT
- **GET**     list of files uploaded
- **GET**     files by cid
- **GET**     status from filecoin

## Prequisites

- [web3](https://pypi.org/project/web3/) - web3 python package to process contract 
- Polygon Mainnet Wallet - [Metamask Tutorial](https://docs.filswan.com/getting-started/beginner-walkthrough/public-testnet/setup-metamask)
- Polygon Mainnet RPC endpoint - [Signup via Alchemy](https://www.alchemy.com/) or use https://polygon-rpc.com/ (you will also need USDC and MATIC balance to use this SDK.)

# MCS API

For more information about API usage, check out the MCS API documentation (https://docs.filswan.com/development-resource/mcp-api).

# Usage

Instructions for developers working with MCS SDK and API.

## Installation

### Method 1. Using GitHub
Install python SDK from GitHub (checkout to the main branch for mainnet support) and install requirements using pip

```
git clone https://github.com/filswan/python-mcs-sdk.git
git checkout main
pip install -r requirements.txt
```

### Method 2. Using Pip
Install python SDK using pip https://pypi.org/project/python-mcs-sdk/

```
pip install python-mcs-sdk
```

## Getting Started

This is a demo for users to use the simplified MCS upload functions `MCSUpload`. For the complete [documentation](#documentation).

### MCS upload
You can use the `MCSUpload` class in `upload/mcs_upload.py` to upload a file or as a simple example for accessing MCS API and smart contract.

The `MCSUpload` contains functions:
- `__init__()`: 
  - parameters:  `chain_name`, `wallet_address`, `private_key`, `rpc_endpoint`, `file_path`
  - initialize the upload function using wallet info and file_path
- `approve_token()`:
  - parameters: `amount`
  - return: txhash for approve
  - change the approved amount (this value will be reset to the amount rather than increment)
- `stream_upload()`:
  - return: API response from MCS upload
  - Upload file to MCS, this function will return an `is_free` variable and the payment is not required payment when `need_pay==0`
- `estimate_amount()`:
  - return: estimated lockin payment
  - can be used to check the payment amount after uploading a file (upload will not be processed until the payment is made through smart contract)
- `pay()`:
  - return: payment success/payment failed with an error message
  - this function calls the payment contract to pay for the currently processing upload (info stored in upload_response)
- `mint()`:
  - parameters: `file_name`
  - return: `tx_hash`, `token_id`, MCS mint update API response
  - this function allows to mint NFT to open sea

### Create File
Let's create `demo.py` to run the demo code.

### Set Up Wallet Information
First, you should set up your wallet address, private key and web3 API. (They can be put into a `.env` file)
```
wallet_address="<WALLET_ADDRESS>"
private_key="<PRIVATE_KEY>"
rpc_endpoint="<RPC_ENDPOINT>"
```

### Initialize Upload
To start an upload, we need to create an instance of the `MCSUpload` class. Which requires `chain_name`, `wallet_address`, `private_key` and `file_path` as 
parameters. The upload process requires the user login into the MCS API using a wallet address. Python MCS SDK can handle this process automatically when initializing
an MCSUpload.

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

The upload function uploads the file to the IPFS server. MCS currently has 10GB of free upload per month for each wallet. The `need_pay` will indicates if a file is under 
the coverage of free upload. When `need_pay == 1` then the file needs to be paid and it is free when `need_pay == 0`.

### Approve Token
Before processing payment we need to approve enough tokens for the upload payment and gas fee. You don't need to approve any token if the upload is free. You can also choose how much you want to approve based on the estimated price.

```python
upload.approve_token(<amount>)
```

### Estimate Payment
The estimated payment can be accessed using the `estimate_amount()` function.

```python
print(upload.estimate_amount())
```

### Payment
Currently, on MCS mainnet, users only need to pay if the upload surpasses the free upload coverage. However,  users can still force a payment after upload (This is not recommended).

```python
if need_pay:
  upload.pay()
```

### Full Demo Code
To use the full demo code, you will need to add your wallet info and add the `amount` and `file_path` in the following script.

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

## Documentation

For more examples please see the [SDK documentation](https://docs.filswan.com/multi-chain-storage/developer-quickstart/sdk)

# Contributing

Feel free to join in and discuss. Suggestions are welcome! [Open an issue](https://github.com/filswan/python-mcs-sdk/issues) or [Join the Discord](https://discord.com/invite/KKGhy8ZqzK)!

## Sponsors

This project is sponsored by Filecoin Foundation

[Flink SDK - A data provider offers Chainlink Oracle service for Filecoin Network ](https://github.com/filecoin-project/devgrants/issues/463)

<img src="https://github.com/filswan/flink/blob/main/filecoin.png" width="200">
