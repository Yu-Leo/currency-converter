import datetime

import redis

from . import exceptions
from .IDatabase import IDatabase


class RedisDatabase(IDatabase):
    """
    Class for working with Redis database
    """
    _CURRENCY_LIST_NAME = 'currencies'
    _DATE_FIELD_NAME = 'date'

    def __init__(self, host: str, port: int, db: int):
        self._redis_client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def __del__(self):
        self._redis_client.close()

    @staticmethod
    def catch_exceptions(func):
        def _wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except redis.RedisError:
                raise exceptions.DatabaseError

        return _wrapper

    @catch_exceptions
    def set_all_data(self, date: datetime.date, currencies_list: tuple[str],
                     currencies_values: dict[str, float]) -> None:
        self._set_date(date)
        self._set_currencies_list(currencies_list)
        self._set_currencies_values(currencies_values)

    @catch_exceptions
    def is_currency_value_exists(self, key: str) -> bool:
        return bool(self._redis_client.exists(key))

    @catch_exceptions
    def get_currency_value(self, key: str) -> float:
        return float(self._redis_client.get(name=key))

    @catch_exceptions
    def is_currencies_list_exists(self) -> bool:
        return bool(self._redis_client.exists(self._CURRENCY_LIST_NAME))

    @catch_exceptions
    def get_currencies_list(self) -> tuple[str]:
        return tuple(sorted(list(self._redis_client.smembers(name=self._CURRENCY_LIST_NAME))))

    @catch_exceptions
    def get_date(self) -> datetime.date | None:
        date_in_iso_format = self._redis_client.get(name=self._DATE_FIELD_NAME)
        if date_in_iso_format is None:
            return None
        return datetime.date.fromisoformat(date_in_iso_format)

    @catch_exceptions
    def _set_currency_value(self, key: str, value: float) -> None:
        self._redis_client.set(name=key, value=value)

    @catch_exceptions
    def _set_currencies_values(self, values: dict[str, float]) -> None:
        for key, value in values.items():
            self._set_currency_value(key, value)

    @catch_exceptions
    def _set_currencies_list(self, currencies_list: list[str]) -> None:
        self._redis_client.sadd(self._CURRENCY_LIST_NAME, *currencies_list)

    @catch_exceptions
    def _set_date(self, date: datetime.date) -> None:
        self._redis_client.set(name=self._DATE_FIELD_NAME, value=str(date))
