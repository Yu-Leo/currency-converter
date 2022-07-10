import datetime
from abc import ABC, abstractmethod


class IDatabase(ABC):
    """
    Interface for classes working with database
    """

    def set_all_data(self, date: datetime.date, currencies_list: tuple[str],
                     currencies_values: dict[str, float]) -> None:
        pass

    # Currencies values

    @abstractmethod
    def is_currency_value_exists(self, key: str) -> bool:
        """
        :param key: name of currency
        """
        pass

    @abstractmethod
    def get_currency_value(self, key: str) -> float:
        """
        :param key: name of currency
        :return: the cost of one dollar (USD) in the currency
        """
        pass

    # Currencies list

    @abstractmethod
    def is_currencies_list_exists(self) -> bool:
        pass

    @abstractmethod
    def get_currencies_list(self) -> tuple[str]:
        """
        :return: list with names of currencies
        """
        pass

    # Date

    @abstractmethod
    def get_date(self) -> datetime.date | None:
        pass
