import pytest
import os
from mcs.api import McsAPI

wallet_address = "*"


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
    api = McsAPI()
    filepath = "/images/log_mcs.png"
    father_path = os.path.abspath(os.path.dirname(__file__))
    print(api.upload_file(wallet_address, father_path + filepath))
