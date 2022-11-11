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

## Prerequisite

- [web3](https://pypi.org/project/web3/) - web3 python package to process contract 
- Polygon Mainnet Wallet - [Metamask Tutorial](https://docs.filswan.com/getting-started/beginner-walkthrough/public-testnet/setup-metamask)
- Polygon Mainnet RPC endpoint - https://polygon-rpc.com (USDC and Matic is required if you want to make payment.)

# MCS API

For more information about API usage, check out the MCS API documentation (https://docs.filswan.com/development-resource/mcp-api).

# Usage

Instructions for developers working with MCS SDK and API.

## Installation
### Method 1. pip install (Recommended)
Install python SDK using pip https://pypi.org/project/python-mcs-sdk/

```
pip install python-mcs-sdk
```

### Method 2. Build from source
Install python SDK from GitHub (checkout to the main branch for mainnet support) and install requirements using pip
```
git clone https://github.com/filswan/python-mcs-sdk.git
git checkout main
pip install -r requirements.txt
```

## Getting Started

This is a demo for users to use the simplified MCS upload functions `MCSUpload`. For the complete [documentation](#documentation).

### Set Up Wallet Information
Create an `.env` file
```
wallet_address="<WALLET_ADDRESS>"
private_key="<PRIVATE_KEY>"
rpc_endpoint="<RPC_ENDPOINT>"
```
install  python-dotenv

```
pip install python-dotenv
```
### Initialize Upload
To start an upload, we need to create an instance of the `MCSUpload` class. Which requires `chain_name`, `wallet_address`, `private_key` and `file_path` as 
parameters. The upload process requires the user login into the MCS API using a wallet address. Python MCS SDK can handle this process automatically when initializing
an MCSUpload.

```python
import os
from mcs import McsAPI
from dotenv import load_dotenv

load_dotenv(".env")
file_path="./test.py"
upload_handle = MCSUpload("polygon.mainnet", os.getenv('wallet_address'), os.getenv('private_key'), os.getenv('rpc_endpoint'), file_path)
```

### Upload File
To upload the file to MCS, we need to call the `stream_upload()` function.

```python
file_data, need_pay = upload_handle.stream_upload()
```

The upload function uploads the file to the IPFS server. MCS currently has 10GB of free upload per month for each wallet. The `need_pay` will indicates if a file is under 
the coverage of free upload. When `need_pay == 1` then the file needs to be paid and it is free when `need_pay == 0`.

### Approve Token
Before processing payment we need to approve enough tokens for the upload payment and gas fee. You don't need to approve any token if the upload is free. You can also choose how much you want to approve based on the estimated price.

```python
upload_handle.approve_token(<amount>)
```

### Estimate Payment
The estimated payment can be accessed using the `estimate_amount()` function.

```python
print(upload_handle.estimate_amount())
```

### Payment
Currently, on MCS mainnet, users only need to pay if the upload surpasses the free upload coverage. However,  users can still force a payment after upload (This is not recommended).

```python
if need_pay:
  upload_handle.pay()
```

### Full Demo Code
To use the full demo code, you will need to add your wallet info and add the `amount` and `file_path` in the following script.

```python
import os
from dotenv import load_dotenv
from mcs.upload.mcs_upload import MCSUpload

if __name__ == '__main__':
    
    # setup env and wallet
    load_dotenv(".env")

    # Load file path
    file_path = "./test.py"

    # Upload file
    upload_handle = MCSUpload("polygon.mainnet", os.getenv('wallet_address'), os.getenv('private_key'), os.getenv('rpc_endpoint'), file_path)
    file_data, need_pay = upload_handle.stream_upload()

    # Process payment
    if need_pay:
        upload_handle.approve_token(<amount>)
        upload_handle.pay()
    
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
