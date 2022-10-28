import pytest
import os
from dotenv import load_dotenv
from mcs.common.params import Params
from mcs.api import McsAPI


@pytest.mark.asyncio
async def test_get_params():
    api_main = McsAPI(Params().MCS_API)
    print(api_main.get_params())


@pytest.mark.asyncio
async def test_user_register():
    load_dotenv(".env_main")
    wallet_address = os.getenv('wallet_address')
    private_key = os.getenv('private_key')
    api = McsAPI(Params().MCS_API)
    jwt_token = api.get_jwt_token(wallet_address, private_key, "polygon.mainnet")
    print(jwt_token)


@pytest.mark.asyncio
async def test_get_price_rate():
    api_main = McsAPI(Params().MCS_API)
    print(api_main.get_price_rate())

@pytest.mark.asyncio
async def test_upload_file():
    load_dotenv(".env_main")
    wallet_address = os.getenv('wallet_address')
    private_key = os.getenv('private_key')
    print(wallet_address)
    filepath = "/images/log_mcs.png"
    parent_path = os.path.abspath(os.path.dirname(__file__))

    # main net test
    api_main = McsAPI(Params().MCS_API)
    api_main.get_jwt_token(wallet_address, private_key, "polygon.mainnet")
    print(api_main.upload_file(wallet_address, parent_path + filepath))


