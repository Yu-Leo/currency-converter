from typing import NamedTuple

import requests

from . import exceptions
from . import settings
from .ExchangeRateAPI import ExchangeRateAPI
from .IDatabase import IDatabase
from .RedisDatabase import RedisDatabase


class Operation(NamedTuple):
    amount: float
    primary_currency: str
    secondary_currency: str


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


def convert(operation: Operation) -> float:
    currencies_values = _get_currencies_values()
    return _calculate(operation.amount, operation.primary_currency,
                      operation.secondary_currency, currencies_values)


def _get_currencies_values() -> dict[str, float]:
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


def _calculate(amount: float, primary_currency: str, secondary_currency: str, currencies: dict[str, float]) -> float:
    """
    :param amount: amount to be converted
    """
    try:
        return round((currencies[secondary_currency] / currencies[primary_currency]) * amount, 6)
    except ZeroDivisionError:
        raise exceptions.ExchangeRateException
