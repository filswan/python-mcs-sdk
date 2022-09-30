from mcs.common.constants import MCS_MUMBAI_API, MCS_BSC_API
from mcs.api import McsAPI

class Params:

    def __init__(self, chain_name='mumbai'):
        if chain_name == 'mumbai':
            self.MCS_API = MCS_MUMBAI_API
        elif chain_name == 'bsc':
            self.MCS_API = MCS_BSC_API
        else: return 'unknown chain name'

        api = McsAPI(self.MCS_API)
        params = api.get_params()['data']
        self.CHAIN_NAME = params['chain_name']
        self.SWAN_PAYMENT_ADDRESS = params['payment_contract_address']
        self.USDC_TOKEN = params['usdc_address']
        self.MINT_ADDRESS = params['mint_contract_address']
    
    def get_params(self):

        vars = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
        paramdict = {}
        for i in vars:
            paramdict[i] = getattr(self, i)

        return paramdict
    
    def __str__(self):
        return self.get_params

