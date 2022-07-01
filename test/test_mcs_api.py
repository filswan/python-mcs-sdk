import pytest

from mcs.api import McsAPI


@pytest.mark.asyncio
async def test_get_params():
    api = McsAPI()
    print(api.get_params())


@pytest.mark.asyncio
async def test_get_price_rate():
    api = McsAPI()
    print(api.get_price_rate())
