import requests

from IExchangeRateAPI import IExchangeRateAPI
from . import exceptions
from . import settings


class ExchangeRateAPI(IExchangeRateAPI):
    """
    Class for working with ExchangeRateAPI (exchangerate-api.com)
    """

    def __init__(self):
        try:
            resource = requests.get(url=settings.EXCHANGE_RATE_API_URL).json()
            self._currencies_values = resource.get('rates').keys()
        except:
            raise exceptions.APIException

    def get_currencies_values(self) -> dict[str, float]:
        return self._currencies_values

    def get_currencies_list(self) -> list[str]:
        return self._currencies_values.keys()
