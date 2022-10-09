import pytest
import os
from dotenv import load_dotenv
from mcs.common.params import Params
from mcs.api import McsAPI


@pytest.mark.asyncio
async def test_get_params():
    api_main = McsAPI(Params().MCS_API)
    print(api_main.get_params())

    api_mumbai = McsAPI(Params('mumbai').MCS_API)
    print(api_mumbai.get_params())

    api_bsc = McsAPI(Params('bsc').MCS_API)
    print(api_bsc.get_params())


@pytest.mark.asyncio
async def test_user_register():
    load_dotenv(".env_mumbai")
    wallet_address = os.getenv('wallet_address')
    private_key = os.getenv('private_key')
    api_mumbai = McsAPI(Params('mumbai').MCS_API)
    jwt_token = api_mumbai.get_jwt_token(wallet_address, private_key)
    print(jwt_token)


@pytest.mark.asyncio
async def test_get_price_rate():
    api_main = McsAPI(Params('main').MCS_API)
    print(api_main.get_price_rate())

    api_mumbai = McsAPI(Params('mumbai').MCS_API)
    print(api_mumbai.get_price_rate())

    api_bsc = McsAPI(Params('bsc').MCS_API)
    print(api_bsc.get_price_rate())


@pytest.mark.asyncio
async def test_upload_file():
    load_dotenv(".env_mumbai")
    wallet_address = os.getenv('wallet_address')
    print(wallet_address)
    filepath = "/images/log_mcs.png"
    parent_path = os.path.abspath(os.path.dirname(__file__))

    # main net test
    api_main = McsAPI(Params().MCS_API)
    print(api_main.upload_file(wallet_address, parent_path + filepath))

    # mumbai net test
    api_mumbai = McsAPI(Params('mumbai').MCS_API)
    load_dotenv(".env_mumbai")
    wallet_address = os.getenv('wallet_address')
    private_key = os.getenv('private_key')
    api_mumbai.get_jwt_token(wallet_address, private_key)
    print(api_mumbai.upload_file(wallet_address, parent_path + filepath))
    #
    # api_bsc = McsAPI(Params('bsc').MCS_API)
    # print(api_bsc.upload_file(wallet_address, parent_path + filepath))
