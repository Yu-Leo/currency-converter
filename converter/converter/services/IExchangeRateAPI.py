import datetime
from abc import ABC, abstractmethod


class IExchangeRateAPI(ABC):
    """
    Interface for classes working with exchange rate API
    """

    @abstractmethod
    def get_currencies_values(self) -> dict[str, float]:
        """
        :return: currencies rates in dictionary
        ({'currency name': 'the cost of one dollar (USD) in the currency',})
        """
        pass

    @abstractmethod
    def get_currencies_list(self) -> tuple[str]:
        """
        :return: tuple with currencies names
        """
        pass

    @abstractmethod
    def get_date(self) -> datetime.date:
        """
        :return: date of request
        """
        pass
