import datetime
import logging
from typing import NamedTuple

from . import exceptions
from . import settings
from .ExchangeRateAPI import ExchangeRateAPI
from .IDatabase import IDatabase
from .RedisDatabase import RedisDatabase

logger = logging.getLogger('main')


class Operation(NamedTuple):
    amount: float
    primary_currency: str
    secondary_currency: str


def get_currencies_list() -> tuple[str]:
    """
    :return: tuple with currencies names
    """
    try:
        return _get_currencies_list_from_db()
    except exceptions.DatabaseError as db_e:
        logger.error(db_e)
        try:
            return _get_currencies_list_from_api()
        except exceptions.APIError as api_e:
            logger.critical(api_e)
            raise exceptions.GettingDataError


def convert(operation: Operation) -> float:
    primary_currency_value = _get_currency_value(operation.primary_currency)
    secondary_currency_value = _get_currency_value(operation.secondary_currency)
    return _calculate(operation.amount, primary_currency_value, secondary_currency_value)


def _get_currencies_list_from_db() -> tuple[str]:
    """
    :return: tuple with currencies names from database
    """
    database: IDatabase = RedisDatabase(host=settings.REDIS_HOST,
                                        port=settings.REDIS_PORT,
                                        db=settings.REDIS_DB)
    if not database.is_currencies_list_exists():
        _update_data_in_database(database)

    return database.get_currencies_list()


def _get_currencies_list_from_api() -> tuple[str]:
    """
    :return: tuple with currencies names from API
    """
    api = ExchangeRateAPI()
    return api.get_currencies_list()


def _get_currency_value(currency: str) -> float:
    """
    :return: the cost of one dollar (USD) in the 'currency'
    """
    try:
        return _get_currency_value_from_db(currency)
    except exceptions.DatabaseError as db_e:
        logger.error(db_e)
        try:
            return _get_currency_value_from_api(currency)
        except exceptions.APIError as api_e:
            logger.critical(api_e)
            raise exceptions.GettingDataError


def _get_currency_value_from_db(currency: str) -> float:
    database: IDatabase = RedisDatabase(host=settings.REDIS_HOST,
                                        port=settings.REDIS_PORT,
                                        db=settings.REDIS_DB)
    is_currency_value_exists = database.is_currency_value_exists(currency)
    is_todays_date_in_database = database.get_date() == datetime.date.today()

    if not is_currency_value_exists or is_currency_value_exists and not is_todays_date_in_database:
        _update_data_in_database(database)
    return database.get_currency_value(currency)


def _get_currency_value_from_api(currency: str) -> float:
    api = ExchangeRateAPI()
    currencies_values = api.get_currencies_values()
    return currencies_values[currency]


def _calculate(amount: float, primary_currency_value: float, secondary_currency_values: float) -> float:
    """
    :param amount: amount to be converted
    :param primary_currency_value: the cost of one dollar (USD) in the primary_currency
    :param secondary_currency_values: the cost of one dollar (USD) in the secondary_currency
    :return:
    """
    try:
        return round((secondary_currency_values / primary_currency_value) * amount, 6)
    except ZeroDivisionError:
        raise exceptions.ConversionError


def _update_data_in_database(database: IDatabase) -> None:
    try:
        api = ExchangeRateAPI()
    except exceptions.APIError as api_e:
        logger.critical(api_e)
        raise exceptions.GettingDataError
    else:
        database.set_all_data(date=api.get_date(),
                              currencies_list=api.get_currencies_list(),
                              currencies_values=api.get_currencies_values())
