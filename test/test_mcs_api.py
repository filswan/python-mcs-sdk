import pytest
import os
from dotenv import load_dotenv

from mcs.common.constants import MCS_MUMBAI_API, MCS_BSC_API
from mcs.common.params import Params
from mcs.api import McsAPI

load_dotenv()
wallet_address = os.getenv('wallet_address')


@pytest.mark.asyncio
async def test_get_params():
    api_mumbai = McsAPI(Params('mumbai').get_params()['MCS_API'])
    print(api_mumbai.get_params())

    api_bsc = McsAPI(Params('bsc').get_params()['MCS_API'])
    print(api_bsc.get_params())


@pytest.mark.asyncio
async def test_get_price_rate():
    api_mumbai = McsAPI(Params('mumbai').get_params()['MCS_API'])
    print(api_mumbai.get_price_rate())

    api_bsc = McsAPI(Params('bsc').get_params()['MCS_API'])
    print(api_bsc.get_price_rate())


@pytest.mark.asyncio
async def test_upload_file():
    filepath = "/images/log_mcs.png"
    parent_path = os.path.abspath(os.path.dirname(__file__))

    api_mumbai = McsAPI(Params('mumbai').get_params()['MCS_API'])
    print(api_mumbai.upload_file(wallet_address, parent_path + filepath))

    api_bsc = McsAPI(Params('bsc').get_params()['MCS_API'])
    print(api_bsc.upload_file(wallet_address, parent_path + filepath))


@pytest.mark.asyncio
async def test_get_mint_info():
    api_mumbai = McsAPI(Params('mumbai').get_params()['MCS_API'])
    result = api_mumbai.get_mint_info(475706, None, "0xd97dcf5d4bdfcc9893a79376c2345994c8599586fbb9ba278815b050c79423df",
                               "105702", "0x1A1e5AC88C493e0608C84c60b7bb5f04D9cF50B3")
    print(result)

    api_bsc = McsAPI(Params('bsc').get_params()['MCS_API'])
    result = api_bsc.get_mint_info(475706, None, "0xd97dcf5d4bdfcc9893a79376c2345994c8599586fbb9ba278815b050c79423df",
                               "105702", "0x1A1e5AC88C493e0608C84c60b7bb5f04D9cF50B3")
    print(result)
    