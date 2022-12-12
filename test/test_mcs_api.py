import pytest
import os
from dotenv import load_dotenv
from mcs.common.params import Params
from mcs.api import McsAPI

chain_name = 'polygon.mumbai'

@pytest.mark.asyncio
async def test_get_params():
    api_main = McsAPI(Params(chain_name).MCS_API)
    print(api_main.get_params())


@pytest.mark.asyncio
async def test_user_register():
    load_dotenv(".env_test")
    wallet_address = os.getenv('wallet_address')
    private_key = os.getenv('private_key')
    api = McsAPI(Params(chain_name).MCS_API)
    jwt_token = api.get_jwt_token(wallet_address, private_key, chain_name)
    print(jwt_token)


@pytest.mark.asyncio
async def test_get_price_rate():
    api_main = McsAPI(Params(chain_name).MCS_API)
    print(api_main.get_price_rate())

@pytest.mark.asyncio
async def test_upload_file():
    load_dotenv(".env_test")
    wallet_address = os.getenv('wallet_address')
    private_key = os.getenv('private_key')
    print(wallet_address)
    filepath = "/images/log_mcs.png"
    parent_path = os.path.abspath(os.path.dirname(__file__))

    # main net test
    api_main = McsAPI(Params(chain_name).MCS_API)
    api_main.get_jwt_token(wallet_address, private_key, chain_name)
    print(api_main.upload_file(wallet_address, parent_path + filepath))


