from mcs.common.constants import MCS_POLYGON_MUMBAI_API, MCS_BSC_API, MCS_POLYGON_MAIN_API

class Params:
    def __init__(self, chain_name='polygon.mainnet'):
        if chain_name == 'polygon.mainnet' or chain_name == 'main':
            self.MCS_API = MCS_POLYGON_MAIN_API
        elif chain_name == 'polygon.mumbai' or chain_name == 'mumbai':
            self.MCS_API = MCS_POLYGON_MUMBAI_API
        elif chain_name == 'bsc.testnet' or chain_name == 'bsc':
            self.MCS_API = MCS_BSC_API
        else:
            print('unknown chain name')

    def get_params(self):

        param_vars = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
        param_dict = {}
        for i in param_vars:
            param_dict[i] = getattr(self, i)

        return param_dict

    def __str__(self):
        return self.get_params
