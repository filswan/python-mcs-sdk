import pytest

from mcs.contract import ContractAPI


@pytest.mark.asyncio
async def test_approve_usdc():
    web3_api = "https://polygon-mumbai.g.alchemy.com/***"
    api = ContractAPI(web3_api)
    api.approve_usdc("wallet_address", " private_key", "1")
