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
    def get_currencies_list(self) -> list[str]:
        """
        :return: list with currencies names
        """
        pass
