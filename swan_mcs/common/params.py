from swan_mcs.common.constants import MCS_POLYGON_MUMBAI_API, MCS_BSC_API, MCS_POLYGON_MAIN_API
import logging

class Params:
    def __init__(self, is_calibration=False):
        if is_calibration:
            self.MCS_API = MCS_POLYGON_MUMBAI_API
        else:
            self.MCS_API = MCS_POLYGON_MAIN_API

    def get_params(self):

        param_vars = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
        param_dict = {}
        for i in param_vars:
            param_dict[i] = getattr(self, i)

        return param_dict

    def __str__(self):
        return self.get_params
