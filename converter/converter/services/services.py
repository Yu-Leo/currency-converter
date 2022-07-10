from typing import NamedTuple

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
    primary_currency_value, secondary_currency_value = _get_currencies_values(operation.primary_currency,
                                                                              operation.secondary_currency)
    return _calculate(operation.amount, primary_currency_value, secondary_currency_value)


def _get_currencies_values(primary_currency, secondary_currency) -> tuple[float, float]:
    database: IDatabase = RedisDatabase(host=settings.REDIS_HOST,
                                        port=settings.REDIS_PORT,
                                        db=settings.REDIS_DB)

    primary_currency_value = database.get_currency_value(primary_currency)
    secondary_currency_value = database.get_currency_value(secondary_currency)
    return primary_currency_value, secondary_currency_value
    # try:
    #     resource = requests.get(url=settings.EXCHANGE_RATE_API_URL).json()
    #     return resource.get('rates')
    # except:
    #     raise exceptions.APIException


def _calculate(amount: float, primary_currency_value: float, secondary_currency_values: float) -> float:
    """
    :param amount: amount to be converted
    """
    try:
        return round((secondary_currency_values / primary_currency_value) * amount, 6)
    except ZeroDivisionError:
        raise exceptions.ExchangeRateException
