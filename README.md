# python-mcs-sdk

[![Made by FilSwan](https://img.shields.io/badge/made%20by-FilSwan-green.svg)](https://www.filswan.com/)
[![Chat on discord](https://img.shields.io/badge/join%20-discord-brightgreen.svg)](https://discord.com/invite/KKGhy8ZqzK)

# Table of Contents <!-- omit in toc -->

- [Introduction](#introduction)
  - [For Onchain Storage](#onchain)
  - [For Buckets Storage](#buckets)

- [Getting Started](#started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Examples](#examples)
- [Functions](#functions)
- [Contributing](#contributing)

## ℹ️ [Introduction](#introduction)

A python software development kit for the Multi-Chain Storage (MCS) https://www.multichain.storage/ service. It provides a convenient interface for working with the MCS API. 

## 🆕 [Getting Started](#started)

---

* [**Prerequisites**](#prerequisites)

  * [web3](https://pypi.org/project/web3/) - web3 python package to process contract 

  - Polygon Mainnet Wallet - [Metamask Tutorial](https://docs.filswan.com/getting-started/beginner-walkthrough/public-testnet/setup-metamask)

  - Polygon Mainnet RPC endpoint - https://polygon-rpc.com (USDC and Matic are required if you want to make payment.)

  - .env File

    - Create a .env file that includes the following content.

      ```
      api_key="<API_KEY>"
      access_token="<ACCESS_TOKEN>"
      
      ##If you do not use the onchain function, you do not need to configure the following
      private_key="<PRIVATE_KEY>"
      rpc_endpoint="<RPC_ENDPOINT>"
      wallet_address="<WALLET_ADDRESS>"
      ```

      1. ***The "rpc_endpoint" is the one mentioned above***
      2. ***"Private_key" will be obtained from the wallet***
      3. ***The "api_key" and "access_token" can be generated from the [APIKey](https://www.multichain.storage/#/api_key) page***
      4. ***Please save your APIKey and Access Token after you have generated it, as the Token is not allowed to be viewed repeatedly***

  - dotenv

    ```
    `pip install python-dotenv`
    ```

* ## **[Installation](#installation)**

  1. Method 1. Pip install (Recommended):

     Install python SDK using pip https://pypi.org/project/python-mcs-sdk/

     ```
     pip install python-mcs-sdk
     ```

  2. Method 2. Build from source

     Install python SDK from GitHub (checkout to the main branch for main net support) and install requirements using pip:

     ```
     git clone https://github.com/filswan/python-mcs-sdk.git
     git checkout main
     pip install -r requirements.txt
     ```

## 👨‍💻 [Examples](#examples)

---

Here is the demo to get you started; you can get more information in the [SDK documentation.](https://docs.filswan.com/multi-chain-storage/developer-quickstart/sdk)

1. Login to MCS

   ```python
    from mcs import APIClient
    if __name__ == '__main__':
        api_key = os.getenv('api_key')
        access_token = os.getenv('access_token')
        mcs_api = APIClient(api_key, access_token)
   ```

   **For Onchain Storage** 

   ---

   * Init

     ```python
     from mcs import OnchainAPI
     onchain = OnchainAPI(mcs_api)
     ```

   * Upload File to Onchain storage

     ```python
     print(onchain.upload_file('<File Path>'))
     ```

   **For Bucket Storage**

   ---

   * Init

     ```python
     from mcs import BucketAPI
     bucket = BucketAPI(mcs_api)
     ```

   * Create a bucket

     ```python
     print(bucket.create_bucket('<bucket name>'))
     ```

   * Upload a file to the bucket

     ```python
     print(bucket.upload_to_bucket('<bucket_id>', '<file_path>' ,prefix=''))
     ```

     *The prefix field defines the file-folder relationship, leaving it blank if the file exists directly in the Bucket or the folder name if the file exists in a folder that already exists in the Bucket.*

     ***You have to create a bucket before you upload a file.***

     ***Note that if you upload a file with the prefix field defined in a folder that has not yet been created, you will not be able to see the file until you create a folder with the same name.***

For more examples, please see the [SDK documentation.](https://docs.filswan.com/multi-chain-storage/developer-quickstart/sdk)

## ℹ️ [Functions](#functions)

This SDK has the following functionalities:

### [For Onchain Storage](#onchain)

---

- **POST**    Upload file to Filswan IPFS gateway
- **GET**     List of files uploaded
- **GET**     Files by cid
- **GET**     Status from filecoin
- **CONTRACT**    Make payment to swan filecoin storage gateway
- **CONTRACT**    Mint asset as NFT

### [For Buckets Storage](#buckets)

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
