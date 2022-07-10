import datetime
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


def get_currencies_list() -> tuple[str]:
    """
    :return: tuple with currencies from API.
    """
    try:
        database: IDatabase = RedisDatabase(host=settings.REDIS_HOST,
                                            port=settings.REDIS_PORT,
                                            db=settings.REDIS_DB)
        if not database.is_currencies_list_exists():
            _update_data_in_database(database)

        return database.get_currencies_list()
    except exceptions.DatabaseError:
        api = ExchangeRateAPI()
        return api.get_currencies_list()
        # Logs


def convert(operation: Operation) -> float:
    primary_currency_value, secondary_currency_value = _get_currencies_values(operation.primary_currency,
                                                                              operation.secondary_currency)
    return _calculate(operation.amount, primary_currency_value, secondary_currency_value)


def _get_currencies_values(primary_currency, secondary_currency) -> tuple[float, float]:
    try:
        database: IDatabase = RedisDatabase(host=settings.REDIS_HOST,
                                            port=settings.REDIS_PORT,
                                            db=settings.REDIS_DB)
        is_currency_value_exists = database.is_currency_value_exists(primary_currency) and \
                                   database.is_currency_value_exists(secondary_currency)
        is_todays_date_in_database = database.get_date() == datetime.date.today()

        if not is_currency_value_exists or is_currency_value_exists and not is_todays_date_in_database:
            _update_data_in_database(database)
        primary_currency_value = database.get_currency_value(primary_currency)
        secondary_currency_value = database.get_currency_value(secondary_currency)

    except exceptions.DatabaseError:
        api = ExchangeRateAPI()
        currencies_values = api.get_currencies_values()
        primary_currency_value = currencies_values[primary_currency]
        secondary_currency_value = currencies_values[secondary_currency]

    return primary_currency_value, secondary_currency_value


def _calculate(amount: float, primary_currency_value: float, secondary_currency_values: float) -> float:
    """
    :param amount: amount to be converted
    """
    try:
        return round((secondary_currency_values / primary_currency_value) * amount, 6)
    except ZeroDivisionError:
        raise exceptions.ExchangeRateException


def _update_data_in_database(database: IDatabase) -> None:
    api = ExchangeRateAPI()
    database.set_all_data(date=api.get_date(),
                          currencies_list=api.get_currencies_list(),
                          currencies_values=api.get_currencies_values())
