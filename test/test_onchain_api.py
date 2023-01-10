import pytest
import os
from dotenv import load_dotenv
from mcs.common.params import Params
from mcs import OnchainAPI, APIClient

chain_name = 'polygon.mumbai'
load_dotenv('.env_test')
api_key = os.getenv('api_key')
access_token = os.getenv('access_token')

@pytest.mark.asyncio
async def test_get_params():
    mcs_api = APIClient(api_key, access_token, chain_name)
    print(mcs_api.get_params())


@pytest.mark.asyncio
async def test_user_register():
    mcs_api = APIClient(api_key, access_token, chain_name)
    print(mcs_api.token)


@pytest.mark.asyncio
async def test_get_price_rate():
    mcs_api = APIClient(api_key, access_token, chain_name)
    print(mcs_api.get_price_rate())


@pytest.mark.asyncio
async def test_upload_file():
    filepath = "/images/log_mcs.png"
    parent_path = os.path.abspath(os.path.dirname(__file__))

    mcs_api = APIClient(api_key, access_token, chain_name)
    onchain_api = OnchainAPI(mcs_api)
    print(onchain_api.upload_file(parent_path + filepath))


