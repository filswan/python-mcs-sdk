import pytest
import os
from dotenv import load_dotenv

from mcs.api import McsAPI


@pytest.mark.asyncio
async def test_get_params():
    api = McsAPI()
    print(api.get_params())


@pytest.mark.asyncio
async def test_get_price_rate():
    api = McsAPI()
    print(api.get_price_rate())


@pytest.mark.asyncio
async def test_upload_file():
    load_dotenv()
    wallet_address = os.getenv('wallet_address')
    print(wallet_address)
    api = McsAPI()
    filepath = "/images/log_mcs.png"
    parent_path = os.path.abspath(os.path.dirname(__file__))
    print(api.upload_file(wallet_address, parent_path + filepath))

@pytest.mark.asyncio
def test_stream_upload_file_pay():
    load_dotenv()
    wallet_address = os.getenv('wallet_address')
    api = McsAPI()
    # upload file to mcs
    filepath = "/images/log_mcs.png"
    parent_path = os.path.abspath(os.path.dirname(__file__))
    print(api.stream_upload_file(wallet_address, parent_path + filepath))