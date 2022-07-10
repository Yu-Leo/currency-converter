from typing import NamedTuple

import requests

from . import exceptions
from . import settings
from .ExchangeRateAPI import ExchangeRateAPI
from .IDatabase import IDatabase
from .RedisDatabase import RedisDatabase


class Operation(NamedTuple):
    amount: float
    from_currency: str
    to_currency: str


def get_currencies_list() -> list[str]:
    """
    :return: list with currencies from API.
    """
    database: IDatabase = RedisDatabase(host=settings.REDIS_HOST,
                                        port=settings.REDIS_PORT,
                                        db=settings.REDIS_DB)
    if database.is_currencies_list_exists():
        return database.get_currencies_list()

    api = ExchangeRateAPI()
    database.set_currencies_list(api.get_currencies_list())
    database.set_currencies_values(api.get_currencies_values())


def get_currencies_values() -> dict[str, float]:
    """
    :return: dictionary with currencies from API.
    Key - name of currency
    Value - the cost of one dollar (USD) in the currency
    """
    try:
        resource = requests.get(url=settings.EXCHANGE_RATE_API_URL).json()
        return resource.get('rates')
    except:
        raise exceptions.APIException


def convert(amount: float, from_currency: str, to_currency: str, currencies: dict[str, float]) -> float:
    """
    :param amount: amount to be converted
    :param from_currency: currency of the amount to be converted
    :param to_currency: currency to convert to
    :param currencies: dictionary from API
    :return: amount in 'to_currency' currency
    """
    try:
        return round((currencies[to_currency] / currencies[from_currency]) * amount, 6)
    except ZeroDivisionError:
        raise exceptions.ExchangeRateException
