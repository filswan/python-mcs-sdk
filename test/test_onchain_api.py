import pytest
import os
from dotenv import load_dotenv
from mcs.common.params import Params
from mcs import OnchainClient

chain_name = 'polygon.mumbai'

@pytest.mark.asyncio
async def test_get_params():
    api_main = OnchainClient(Params(chain_name).MCS_API)
    print(api_main.get_params())


@pytest.mark.asyncio
async def test_user_register():
    load_dotenv(".env_test")
    api_key = os.getenv('api_key')
    access_token = os.getenv('access_token')
    api = OnchainClient(Params(chain_name).MCS_API)
    jwt_token = api.api_key_login(api_key, access_token, chain_name)
    print(jwt_token)


@pytest.mark.asyncio
async def test_get_price_rate():
    api_key = os.getenv('api_key')
    access_token = os.getenv('access_token')
    api = OnchainClient(Params(chain_name).MCS_API)
    api.api_key_login(api_key, access_token, chain_name)
    print(api.get_price_rate())


@pytest.mark.asyncio
async def test_upload_file():
    load_dotenv(".env_test")
    api_key = os.getenv('api_key')
    access_token = os.getenv('access_token')
    filepath = "/images/log_mcs.png"
    parent_path = os.path.abspath(os.path.dirname(__file__))

    # main net test
    api = OnchainClient(Params(chain_name).MCS_API)
    api.api_key_login(api_key, access_token, chain_name)
    print(api.upload_file(parent_path + filepath))


