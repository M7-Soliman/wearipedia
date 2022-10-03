from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)

from ...devices.device import BaseDevice
from ...utils import seed_everything
from .fenix_fetch import *
from .fenix_gen import *

class_name = "Fenix7S"


class Fenix7S(BaseDevice):
    def __init__(self):
        self._authorized = False
        self.valid_data_types = ["dates", "steps", "hrs", "brpms"]

    def _get_data(self, data_type, params=None):
        if params is None:
            params = {"start_date": "2022-03-01", "end_date": "2022-06-17"}

        if hasattr(self, data_type):
            return getattr(self, data_type)

        return fetch_real_data(params["start_date"], params["end_date"], data_type)

    def gen_synthetic(self, seed=0):
        # generate random data according to seed
        seed_everything(seed)

        self.dates, self.steps, self.hrs, self.brpms = create_syn_data()

    def authorize(self, auth_creds):
        # authorize this device against API

        self.auth_creds = auth_creds

        # Initialize Garmin api with your credentials
        api = Garmin(auth_creds["email"], auth_creds["password"])

        api.login()

        self._authorized = True
