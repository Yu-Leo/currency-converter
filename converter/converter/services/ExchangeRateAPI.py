import datetime

import requests

from . import exceptions
from . import settings
from .IExchangeRateAPI import IExchangeRateAPI


class ExchangeRateAPI(IExchangeRateAPI):
    """
    Class for working with ExchangeRateAPI (exchangerate-api.com)
    """

    def __init__(self):
        try:
            resource = requests.get(url=settings.EXCHANGE_RATE_API_URL).json()
            self._currencies_values = resource.get('rates')
            self._date = resource.get('date')
        except Exception:
            raise exceptions.GettingDataError

    def get_currencies_values(self) -> dict[str, float]:
        return self._currencies_values

    def get_currencies_list(self) -> tuple[str]:
        return tuple(self._currencies_values.keys())

    def get_date(self) -> datetime.date:
        return datetime.date.fromisoformat(self._date)
