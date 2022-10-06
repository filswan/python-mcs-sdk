import pytest
import os
from dotenv import load_dotenv

from mcs.common.constants import MCS_MUMBAI_API, MCS_BSC_API
from mcs.common.params import Params
from mcs.api import McsAPI


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
    load_dotenv()
    wallet_address = os.getenv('wallet_address')
    print(wallet_address)
    api = McsAPI()
    filepath = "/images/log_mcs.png"
    parent_path = os.path.abspath(os.path.dirname(__file__))

    api_mumbai = McsAPI(Params('mumbai').get_params()['MCS_API'])
    print(api_mumbai.upload_file(wallet_address, parent_path + filepath))

    api_bsc = McsAPI(Params('bsc').get_params()['MCS_API'])
    print(api_bsc.upload_file(wallet_address, parent_path + filepath))

@pytest.mark.asyncio
def test_stream_upload_file_pay():
    load_dotenv()
    wallet_address = os.getenv('wallet_address')
    api = McsAPI()
    # upload file to mcs
    filepath = "/images/log_mcs.png"
    parent_path = os.path.abspath(os.path.dirname(__file__))
    print(api.stream_upload_file(wallet_address, parent_path + filepath))